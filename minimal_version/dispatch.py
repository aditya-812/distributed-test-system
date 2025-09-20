#!/usr/bin/env python3
"""
Simple dispatcher script that sends tasks concurrently and prints results.
Uses test-config.yml for orchestration configuration.
"""
from celery_app import task_a, task_b, config

def main():
    # Use configuration loaded by celery_app
    print(f"Loaded config: {config['test_scenario']['description']}")
    print(f"Expected workers: {config['system']['workers']}")
    print("Dispatching tasks...")
    
    # Send both tasks concurrently
    result_a = task_a.delay()
    result_b = task_b.delay()
    
    print(f"Task A sent with ID: {result_a.id}")
    print(f"Task B sent with ID: {result_b.id}")
    
    # Wait for results and print them as required by the challenge
    print("Waiting for results...")
    result_from_a = result_a.get()
    result_from_b = result_b.get()
    
    print(f"Result from task_a: {result_from_a}")
    print(f"Result from task_b: {result_from_b}")

if __name__ == '__main__':
    main()
