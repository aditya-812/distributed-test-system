"""
Minimal Celery application with two tasks and routing.
"""
from celery import Celery

# Celery configuration
app = Celery('minimal_test_system')
app.conf.update(
    broker_url='pyamqp://guest@localhost//',
    result_backend='rpc://',
    task_routes={
        'celery_app.task_a': {'queue': 'queue_a'},
        'celery_app.task_b': {'queue': 'queue_b'},
    },
)

@app.task
def task_a():
    """Task A: Returns greeting message."""
    return "Hello from Task A"

@app.task
def task_b():
    """Task B: Returns greeting message."""
    return "Hello from Task B"

if __name__ == '__main__':
    app.start()
