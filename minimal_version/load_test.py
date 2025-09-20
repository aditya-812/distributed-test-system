#!/usr/bin/env python3
"""
Load testing script to demonstrate horizontal scaling benefits.
Sends multiple tasks to test worker capacity and scaling.
"""
import time
from celery_app import task_a, task_b, config

def run_load_test(num_tasks: int = 20):
    """Run load test by sending multiple tasks of each type."""
    print(f"Starting load test with {num_tasks} tasks of each type...")
    print(f"Expected workers: {config['system']['workers']}")
    print("-" * 50)
    
    start_time = time.time()
    
    # Send all tasks concurrently (both types)
    print(f"Sending {num_tasks} Task A tasks...")
    tasks_a = [task_a.delay() for _ in range(num_tasks)]
    
    print(f"Sending {num_tasks} Task B tasks...")
    tasks_b = [task_b.delay() for _ in range(num_tasks)]
    
    # Wait for all Task A results
    print("Waiting for Task A results...")
    results_a = []
    for i, task in enumerate(tasks_a):
        try:
            result = task.get()
            results_a.append(result)
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{num_tasks} Task A tasks")
        except Exception as e:
            print(f"  Error in Task A {i + 1}: {e}")
    
    # Wait for all Task B results
    print("Waiting for Task B results...")
    results_b = []
    for i, task in enumerate(tasks_b):
        try:
            result = task.get()
            results_b.append(result)
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{num_tasks} Task B tasks")
        except Exception as e:
            print(f"  Error in Task B {i + 1}: {e}")
    
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
        run_load_test(args.tasks)
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user")
    except Exception as e:
        print(f"Load test failed: {e}")

if __name__ == '__main__':
    main()
