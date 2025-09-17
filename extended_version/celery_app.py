"""
Celery application with distributed task routing and structured logging.
"""
import os
import time
import logging
import json
from datetime import datetime, timezone
from celery import Celery
from celery.utils.log import get_task_logger
from pythonjsonlogger import jsonlogger

# Configure structured logging
def setup_logging():
    """Set up structured JSON logging for Celery tasks."""
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    
    # Custom JSON formatter with additional fields
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
            log_record['timestamp'] = datetime.now(timezone.utc).isoformat()
            log_record['service'] = 'celery-worker'
            log_record['worker_id'] = os.getenv('WORKER_ID', 'unknown')
            
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(service)s %(worker_id)s %(levelname)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Set up logging
setup_logging()

# Celery configuration
BROKER_URL = os.getenv('BROKER_URL', 'pyamqp://guest@localhost//')

app = Celery('distributed_test_system')

# Celery configuration
app.conf.update(
    broker_url=BROKER_URL,
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task routing - direct tasks to specific queues
    task_routes={
        'celery_app.task_a': {'queue': 'queue_a'},
        'celery_app.task_b': {'queue': 'queue_b'},
    },
    
    # Retry configuration
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # Monitoring
    task_track_started=True,
    task_send_sent_event=True,
)

# Get task logger for structured logging
logger = get_task_logger(__name__)

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def task_a(self):
    """
    Task A: Returns greeting message with execution metadata.
    Only processed by workers listening to queue_a.
    """
    start_time = time.time()
    worker_id = os.getenv('WORKER_ID', 'worker-a')
    
    logger.info(
        "Starting task_a execution",
        extra={
            'task_id': self.request.id,
            'task_name': 'task_a',
            'worker_id': worker_id,
            'queue': 'queue_a',
            'retry_count': self.request.retries
        }
    )
    
    # Simulate some work
    time.sleep(0.5)
    
    execution_time = time.time() - start_time
    result = {
        'message': 'Hello from Task A',
        'task_id': self.request.id,
        'worker_id': worker_id,
        'execution_time': round(execution_time, 3),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'queue': 'queue_a'
    }
    
    logger.info(
        "Completed task_a execution",
        extra={
            'task_id': self.request.id,
            'execution_time': execution_time,
            'result': result
        }
    )
    
    return result

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def task_b(self):
    """
    Task B: Returns greeting message with execution metadata.
    Only processed by workers listening to queue_b.
    """
    start_time = time.time()
    worker_id = os.getenv('WORKER_ID', 'worker-b')
    
    logger.info(
        "Starting task_b execution",
        extra={
            'task_id': self.request.id,
            'task_name': 'task_b',
            'worker_id': worker_id,
            'queue': 'queue_b',
            'retry_count': self.request.retries
        }
    )
    
    # Simulate some work
    time.sleep(0.7)
    
    execution_time = time.time() - start_time
    result = {
        'message': 'Hello from Task B',
        'task_id': self.request.id,
        'worker_id': worker_id,
        'execution_time': round(execution_time, 3),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'queue': 'queue_b'
    }
    
    logger.info(
        "Completed task_b execution",
        extra={
            'task_id': self.request.id,
            'execution_time': execution_time,
            'result': result
        }
    )
    
    return result

if __name__ == '__main__':
    app.start()
