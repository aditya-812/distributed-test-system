#!/usr/bin/env python3
"""
Distributed Task Dispatcher

This script sends tasks concurrently to different Celery workers and displays
results with enhanced visualization and structured logging.
"""
import os
import sys
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple

try:
    from colorama import Fore, Back, Style, init
    from celery import Celery
    init(autoreset=True)  # Initialize colorama for cross-platform colored output
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

# Import our Celery app
try:
    from celery_app import app, task_a, task_b
except ImportError:
    print("Error: Could not import celery_app. Make sure celery_app.py is in the current directory.")
    sys.exit(1)

class TaskDispatcher:
    """Enhanced task dispatcher with visualization and monitoring."""
    
    def __init__(self):
        self.app = app
        self.results = []
        self.start_time = None
        self.total_time = None
        
    def print_header(self):
        """Print a styled header for the dispatcher."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🚀 DISTRIBUTED TASK SYSTEM DISPATCHER")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}Broker: {self.app.conf.broker_url}")
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def print_task_status(self, task_name: str, status: str, details: str = ""):
        """Print formatted task status updates."""
        status_colors = {
            'SENT': Fore.BLUE,
            'PENDING': Fore.YELLOW,
            'SUCCESS': Fore.GREEN,
            'FAILURE': Fore.RED,
            'RETRY': Fore.MAGENTA
        }
        
        color = status_colors.get(status, Fore.WHITE)
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"{Fore.WHITE}[{timestamp}] {color}{status:<8} {Fore.CYAN}{task_name:<10} {details}")
    
    def execute_task(self, task_func, task_name: str) -> Tuple[str, Dict[Any, Any]]:
        """Execute a single task and return results."""
        try:
            self.print_task_status(task_name, 'SENT', 'Dispatching task...')
            
            # Send task asynchronously
            async_result = task_func.delay()
            task_id = async_result.id
            
            self.print_task_status(task_name, 'PENDING', f'Task ID: {task_id}')
            
            # Wait for result with timeout
            result = async_result.get(timeout=30)
            
            self.print_task_status(task_name, 'SUCCESS', f'Completed in {result.get("execution_time", "N/A")}s')
            
            return task_name, {
                'status': 'success',
                'result': result,
                'task_id': task_id,
                'async_result': async_result
            }
            
        except Exception as e:
            self.print_task_status(task_name, 'FAILURE', f'Error: {str(e)}')
            return task_name, {
                'status': 'error',
                'error': str(e),
                'task_id': getattr(async_result, 'id', 'unknown') if 'async_result' in locals() else 'unknown'
            }
    
    def display_results(self, results: Dict[str, Dict]):
        """Display formatted results with visualization."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}📊 EXECUTION RESULTS")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Summary statistics
        successful_tasks = sum(1 for r in results.values() if r['status'] == 'success')
        failed_tasks = len(results) - successful_tasks
        
        print(f"{Fore.WHITE}Total Execution Time: {Fore.GREEN}{self.total_time:.3f}s")
        print(f"{Fore.WHITE}Successful Tasks: {Fore.GREEN}{successful_tasks}")
        print(f"{Fore.WHITE}Failed Tasks: {Fore.RED if failed_tasks > 0 else Fore.GREEN}{failed_tasks}")
        
        print(f"\n{Fore.YELLOW}{'─'*60}")
        print(f"{Fore.YELLOW}DETAILED RESULTS")
        print(f"{Fore.YELLOW}{'─'*60}")
        
        for task_name, task_result in results.items():
            if task_result['status'] == 'success':
                result_data = task_result['result']
                print(f"\n{Fore.GREEN}✅ {task_name.upper()}")
                print(f"   {Fore.WHITE}Message: {Fore.CYAN}{result_data['message']}")
                print(f"   {Fore.WHITE}Worker: {Fore.YELLOW}{result_data.get('worker_id', 'N/A')}")
                print(f"   {Fore.WHITE}Queue: {Fore.MAGENTA}{result_data.get('queue', 'N/A')}")
                print(f"   {Fore.WHITE}Task ID: {Fore.BLUE}{result_data.get('task_id', 'N/A')}")
                print(f"   {Fore.WHITE}Execution Time: {Fore.GREEN}{result_data.get('execution_time', 'N/A')}s")
                print(f"   {Fore.WHITE}Timestamp: {Fore.CYAN}{result_data.get('timestamp', 'N/A')}")
            else:
                print(f"\n{Fore.RED}❌ {task_name.upper()}")
                print(f"   {Fore.WHITE}Error: {Fore.RED}{task_result['error']}")
                print(f"   {Fore.WHITE}Task ID: {Fore.BLUE}{task_result.get('task_id', 'N/A')}")
        
        # Performance metrics
        if successful_tasks > 0:
            execution_times = [
                r['result']['execution_time'] 
                for r in results.values() 
                if r['status'] == 'success' and 'execution_time' in r['result']
            ]
            
            if execution_times:
                avg_time = sum(execution_times) / len(execution_times)
                max_time = max(execution_times)
                min_time = min(execution_times)
                
                print(f"\n{Fore.YELLOW}{'─'*60}")
                print(f"{Fore.YELLOW}PERFORMANCE METRICS")
                print(f"{Fore.YELLOW}{'─'*60}")
                print(f"{Fore.WHITE}Average Task Time: {Fore.GREEN}{avg_time:.3f}s")
                print(f"{Fore.WHITE}Fastest Task: {Fore.GREEN}{min_time:.3f}s")
                print(f"{Fore.WHITE}Slowest Task: {Fore.YELLOW}{max_time:.3f}s")
        
        print(f"\n{Fore.CYAN}{'='*60}")
    
    def check_broker_connection(self):
        """Check if the broker is accessible."""
        try:
            # Try to get broker info
            inspect = self.app.control.inspect()
            stats = inspect.stats()
            if stats:
                print(f"{Fore.GREEN}✅ Broker connection successful")
                print(f"{Fore.WHITE}Active workers: {len(stats)}")
                for worker, worker_stats in stats.items():
                    print(f"   {Fore.CYAN}• {worker}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️  No active workers found")
                return True  # Broker is accessible but no workers
        except Exception as e:
            print(f"{Fore.RED}❌ Broker connection failed: {e}")
            print(f"{Fore.YELLOW}💡 Make sure RabbitMQ is running and workers are started")
            return False
    
    def run(self):
        """Main execution method."""
        self.print_header()
        
        # Check broker connection
        if not self.check_broker_connection():
            print(f"\n{Fore.RED}Exiting due to broker connection issues.")
            return
        
        print(f"\n{Fore.CYAN}🎯 DISPATCHING TASKS CONCURRENTLY...")
        print(f"{Fore.CYAN}{'─'*60}")
        
        self.start_time = time.time()
        
        # Define tasks to execute
        tasks = [
            (task_a, 'task_a'),
            (task_b, 'task_b')
        ]
        
        results = {}
        
        # Execute tasks concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self.execute_task, task_func, task_name): task_name
                for task_func, task_name in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task_name, result = future.result()
                results[task_name] = result
        
        self.total_time = time.time() - self.start_time
        
        # Display results
        self.display_results(results)
        
        # Save results to JSON file for further analysis
        self.save_results_to_file(results)
        
        print(f"{Fore.GREEN}🎉 Dispatch completed successfully!\n")
    
    def save_results_to_file(self, results: Dict[str, Dict]):
        """Save execution results to a JSON file for analysis."""
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'total_execution_time': self.total_time,
            'broker_url': self.app.conf.broker_url,
            'results': results
        }
        
        # Make results JSON serializable
        for task_name, task_result in output_data['results'].items():
            if 'async_result' in task_result:
                del task_result['async_result']  # Remove non-serializable object
        
        filename = f"dispatch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"{Fore.BLUE}📄 Results saved to: {filename}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Could not save results to file: {e}")

def main():
    """Main entry point."""
    dispatcher = TaskDispatcher()
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
