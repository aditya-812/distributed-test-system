#!/usr/bin/env python3
"""
Simple dispatcher script that sends tasks concurrently and prints results.
"""
from celery_app import task_a, task_b

def main():
    print("Dispatching tasks...")
    
    # Send both tasks
    result_a = task_a.delay()
    result_b = task_b.delay()
    
    # Get results
    print(f"Result from task_a: {result_a.get()}")
    print(f"Result from task_b: {result_b.get()}")

if __name__ == '__main__':
    main()
