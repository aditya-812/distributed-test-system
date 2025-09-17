# Minimal Distributed Test System

A bare minimum implementation of the distributed test system challenge.

## Requirements

- RabbitMQ running locally
- Docker and Docker Compose
- Python 3.11+

## Setup

1. **Start RabbitMQ**:
   ```bash
   brew services start rabbitmq  # macOS
   # or
   sudo systemctl start rabbitmq-server  # Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build and start workers**:
   ```bash
   docker-compose up -d
   ```

4. **Run dispatcher**:
   ```bash
   python dispatch.py
   ```

## Expected Output

```
Dispatching tasks...
Result from task_a: Hello from Task A
Result from task_b: Hello from Task B
```

## Architecture

- **task_a**: Processed only by worker-a (queue_a)
- **task_b**: Processed only by worker-b (queue_b)
- **RabbitMQ**: Message broker running on host
- **Docker**: Two isolated worker containers

## Files

- `celery_app.py`: Celery configuration and tasks
- `dispatch.py`: Simple dispatcher script
- `Dockerfile`: Worker container definition
- `docker-compose.yml`: Container orchestration
- `requirements.txt`: Python dependencies

## Cleanup

```bash
docker-compose down
```
