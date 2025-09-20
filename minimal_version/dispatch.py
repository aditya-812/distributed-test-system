#!/usr/bin/env python3
"""
Simple dispatcher script that sends tasks concurrently and prints results.
Uses test-config.yml for orchestration configuration.
"""
import time
from celery_app import task_a, task_b, config

def main():
    # Use configuration loaded by celery_app
    print(f"Loaded config: {config['test_scenario']['description']}")
    print(f"Expected workers: {config['system']['workers']}")
    print("Dispatching tasks...")
    
    # Send both tasks concurrently
    start_time = time.time()
    result_a = task_a.delay()
    result_b = task_b.delay()
    
    print(f"Task A sent with ID: {result_a.id}")
    print(f"Task B sent with ID: {result_b.id}")
    
    # Wait for results and print them as required by the challenge
    print("Waiting for results...")
    result_from_a = result_a.get()
    result_from_b = result_b.get()
    
    total_time = time.time() - start_time
    
    # Display results with monitoring information
    print(f"Result from task_a: {result_from_a['result']}")
    print(f"Task A execution time: {result_from_a['execution_time']:.3f}s")
    print(f"Result from task_b: {result_from_b['result']}")
    print(f"Task B execution time: {result_from_b['execution_time']:.3f}s")
    print(f"Total dispatcher time: {total_time:.3f}s (concurrent execution)")
    print(f"Sequential time would be: {result_from_a['execution_time'] + result_from_b['execution_time']:.3f}s")

if __name__ == '__main__':
    main()
