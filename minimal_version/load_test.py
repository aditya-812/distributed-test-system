#!/usr/bin/env python3
"""
Load testing script to demonstrate horizontal scaling benefits.
Sends multiple tasks concurrently to test worker capacity.
"""
import time
import asyncio
import concurrent.futures
from celery_app import task_a, task_b, config

async def send_tasks_async(num_tasks: int, task_func, task_name: str):
    """Send multiple tasks asynchronously."""
    print(f"Sending {num_tasks} {task_name} tasks...")
    start_time = time.time()
    
    # Send all tasks concurrently
    tasks = [task_func.delay() for _ in range(num_tasks)]
    
    # Wait for all results
    results = []
    for i, task in enumerate(tasks):
        try:
            result = task.get()
            results.append(result)
            if (i + 1) % 10 == 0:  # Progress indicator
                print(f"  Completed {i + 1}/{num_tasks} {task_name} tasks")
        except Exception as e:
            print(f"  Error in {task_name} task {i + 1}: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"{task_name} Results:")
    print(f"  Total tasks: {len(results)}")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Average time per task: {total_time/len(results):.3f}s")
    print(f"  Tasks per second: {len(results)/total_time:.2f}")
    
    return results, total_time

async def run_load_test(num_tasks: int = 20):
    """Run load test with both task types."""
    print(f"Starting load test with {num_tasks} tasks of each type...")
    print(f"Expected workers: {config['system']['workers']}")
    print("-" * 50)
    
    # Run both task types concurrently
    start_time = time.time()
    
    # Create tasks for both types
    task_a_coroutine = send_tasks_async(num_tasks, task_a, "Task A")
    task_b_coroutine = send_tasks_async(num_tasks, task_b, "Task B")
    
    # Wait for both to complete
    (results_a, time_a), (results_b, time_b) = await asyncio.gather(
        task_a_coroutine, task_b_coroutine
    )
    
    total_time = time.time() - start_time
    
    print("-" * 50)
    print("Load Test Summary:")
    print(f"  Total tasks sent: {num_tasks * 2}")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Overall throughput: {(num_tasks * 2) / total_time:.2f} tasks/sec")
    print(f"  Task A average execution: {sum(r['execution_time'] for r in results_a) / len(results_a):.3f}s")
    print(f"  Task B average execution: {sum(r['execution_time'] for r in results_b) / len(results_b):.3f}s")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Load test the distributed system')
    parser.add_argument('--tasks', '-t', type=int, default=20, 
                       help='Number of tasks of each type to send (default: 20)')
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_load_test(args.tasks))
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user")
    except Exception as e:
        print(f"Load test failed: {e}")

if __name__ == '__main__':
    main()
