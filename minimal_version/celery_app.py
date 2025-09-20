"""
Minimal Celery application with two tasks and routing.
Uses test-config.yml for configuration.
"""
import os
import yaml
from celery import Celery

def load_config():
    """Load configuration from test-config.yml."""
    config_file = 'test-config.yml'
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found. Cannot start application.")
    
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load {config_file}: {e}")

# Load configuration (required)
config = load_config()

# Build broker URL from config
rabbitmq_config = config['rabbitmq']

# Check if we're running in Docker (environment variable set by docker-compose)
if os.getenv('BROKER_URL'):
    # Use Docker environment variable (for containerized workers)
    broker_url = os.getenv('BROKER_URL')
else:
    # Use config for host connections (for dispatch.py running on host)
    broker_url = f"pyamqp://{rabbitmq_config['username']}@{rabbitmq_config['host']}:{rabbitmq_config['port']}//"

# Build task routes from config
task_routes = {
    f'celery_app.{task}': {'queue': queue} 
    for task, queue in config['task_routing'].items()
}

# Celery configuration
app = Celery('minimal_test_system')
app.conf.update(
    broker_url=broker_url,
    result_backend='rpc://',
    task_routes=task_routes,
)

@app.task
def task_a():
    """Task A: Returns greeting message."""
    return "Hello from Task A"

@app.task
def task_b():
    """Task B: Returns greeting message."""
    return "Hello from Task B"

