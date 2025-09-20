#!/usr/bin/env python3
"""
Dynamic scaling script for the distributed test system.
Supports horizontal scaling of workers based on configuration.
"""
import os
import sys
import yaml
import subprocess
import argparse
from typing import Dict, List

def load_config():
    """Load configuration from test-config.yml."""
    config_file = 'test-config.yml'
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def get_current_workers():
    """Get current running worker containers."""
    try:
        result = subprocess.run(['docker-compose', 'ps', '--services', '--filter', 'status=running'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []

def scale_workers(queue_name: str, count: int, config: Dict):
    """Scale workers for a specific queue."""
    if not config['system']['scaling']['enabled']:
        print(f"Scaling is disabled in configuration.")
        return False
    
    max_workers = config['system']['scaling']['max_workers_per_queue']
    if count > max_workers:
        print(f"Warning: Requested {count} workers exceeds max {max_workers} per queue.")
        count = max_workers
    
    print(f"Scaling {queue_name} workers to {count} instances...")
    
    try:
        # Use docker-compose up --scale to scale workers
        cmd = ['docker-compose', 'up', '-d', '--scale', f'{queue_name}={count}']
        subprocess.run(cmd, check=True)
        print(f"Successfully scaled {queue_name} to {count} workers.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error scaling workers: {e}")
        return False

def scale_all_workers(count: int, config: Dict):
    """Scale all worker types to the same count."""
    queues = list(config['task_routing'].keys())
    success = True
    
    for queue in queues:
        queue_name = f"worker-{queue.split('_')[1]}"  # task_a -> worker-a
        if not scale_workers(queue_name, count, config):
            success = False
    
    return success

def show_status():
    """Show current scaling status."""
    current_workers = get_current_workers()
    print("Current worker status:")
    print(f"Running containers: {len(current_workers)}")
    for worker in current_workers:
        print(f"  - {worker}")
    
    # Show docker-compose ps output
    try:
        result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True, check=True)
        print("\nDetailed status:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting detailed status: {e}")

def main():
    parser = argparse.ArgumentParser(description='Scale distributed test system workers')
    parser.add_argument('action', choices=['scale', 'status', 'scale-all'], 
                       help='Action to perform')
    parser.add_argument('--queue', '-q', help='Queue name (e.g., queue_a, queue_b)')
    parser.add_argument('--count', '-c', type=int, help='Number of workers')
    parser.add_argument('--all-count', '-a', type=int, help='Scale all workers to this count')
    
    args = parser.parse_args()
    
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)
    
    if args.action == 'status':
        show_status()
    elif args.action == 'scale':
        if not args.queue or not args.count:
            print("Error: --queue and --count are required for scale action")
            sys.exit(1)
        scale_workers(args.queue, args.count, config)
    elif args.action == 'scale-all':
        if not args.all_count:
            print("Error: --all-count is required for scale-all action")
            sys.exit(1)
        scale_all_workers(args.all_count, config)

if __name__ == '__main__':
    main()
