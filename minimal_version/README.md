# Minimal Distributed Test System

A bare minimum implementation of the distributed test system challenge.

## Requirements

- RabbitMQ running locally
- Docker and Docker Compose
- Python 3.11+

## Quick Start with Makefile

The easiest way to run the system:

```bash
make test    # Complete automated test
```

Or step by step:
```bash
make up      # Start containers
make run     # Run dispatcher
make down    # Stop containers
```

## Manual Setup

1. **Start RabbitMQ**:
   ```bash
   brew services start rabbitmq  # macOS
   # or
   sudo systemctl start rabbitmq-server  # Linux
   ```

2. **Install dependencies**:
   ```bash
   make install  # Creates venv and installs dependencies
   ```

3. **Build and start workers**:
   ```bash
   docker-compose up -d
   ```

4. **Run dispatcher**:
   ```bash
   python dispatch.py
   ```

## Makefile Commands

```bash
make help       # Show usage
make install    # Install dependencies in virtual environment
make build      # Build containers
make up         # Start containers
make down       # Stop containers
make run        # Run dispatcher
make test       # Full test sequence
make logs       # Show logs
make ps         # Container status
make clean      # Clean up (includes removing venv)
```

## Configuration

The system uses `test-config.yml` for orchestration configuration. The dispatcher loads this file using PyYAML's safe_load method.

## Expected Output

```
Loaded config: Basic two-task execution test
Expected workers: 2
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
- `test-config.yml`: Orchestration configuration file

## Cleanup

```bash
docker-compose down
```
