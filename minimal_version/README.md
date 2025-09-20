# Minimal Distributed Test System

A clean, production-ready implementation of the distributed test system challenge with retry mechanisms, horizontal scaling, and basic monitoring.

## Features

- ✅ **Core Requirements**: RabbitMQ + Celery + Docker isolation
- ✅ **Retry Mechanism**: Automatic retries with exponential backoff
- ✅ **Horizontal Scaling**: Dynamic worker scaling capabilities
- ✅ **Basic Monitoring**: Task execution timing and retry tracking
- ✅ **Load Testing**: Built-in performance testing tools
- ✅ **Configuration**: YAML-based orchestration configuration

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
Task A sent with ID: ce70d64d-fb74-4721-be58-0343624e1f15
Task B sent with ID: 2d726401-9c21-4a2a-8838-d86993c974e9
Waiting for results...
Result from task_a: Hello from Task A
Task A execution time: 0.106s
Task A retries: 0
Result from task_b: Hello from Task B
Task B execution time: 0.202s
Task B retries: 0
Total dispatcher time: 0.340s (concurrent execution)
Sequential time would be: 0.307s
Total retries: 0
```

## Monitoring & Retries

The system includes basic monitoring and retry features:
- **Task execution timing** - Shows how long each task takes to execute
- **Retry mechanism** - Automatic retries with exponential backoff (max 3 retries)
- **Retry tracking** - Shows retry count for each task
- **Total dispatcher time** - Overall time from dispatch to completion
- **Real-time logs** - Use `make monitor` to watch worker logs

## Horizontal Scaling

The system supports dynamic horizontal scaling:

```bash
# Scale individual worker types
make scale QUEUE=worker-a COUNT=3
make scale QUEUE=worker-b COUNT=2

# Scale all workers equally
make scale-all COUNT=4

# Check scaling status
make status

# Run load tests
make load-test TASKS=20
```

See [SCALING.md](SCALING.md) for detailed scaling documentation.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   dispatch.py   │    │   RabbitMQ      │    │  Docker Workers │
│   (Dispatcher)  │────│   (Broker)      │────│                 │
│                 │    │                 │    │  ┌─────────────┐│
└─────────────────┘    │  ┌──────────────┤    │  │  Worker A   ││
                       │  │   queue_a    │◄───┤  │ (task_a)    ││
                       │  │              │    │  └─────────────┘│
                       │  ├──────────────┤    │  ┌─────────────┐│
                       │  │   queue_b    │◄───┤  │  Worker B   ││
                       │  │              │    │  │ (task_b)    ││
                       │  └──────────────┘    │  └─────────────┘│
                       └─────────────────┘    └─────────────────┘
```

- **task_a**: Processed only by worker-a (queue_a) with retry support
- **task_b**: Processed only by worker-b (queue_b) with retry support
- **RabbitMQ**: Message broker running on host
- **Docker**: Scalable worker containers with horizontal scaling
- **Retry Logic**: Automatic retries with exponential backoff (max 3 retries)
- **Monitoring**: Execution timing and retry count tracking

## Files

- `celery_app.py`: Celery configuration with retry mechanisms
- `dispatch.py`: Dispatcher with monitoring and retry tracking
- `Dockerfile`: Worker container definition
- `docker-compose.yml`: Container orchestration
- `requirements.txt`: Python dependencies (celery, pyyaml)
- `test-config.yml`: Orchestration configuration with scaling settings
- `scale.py`: Dynamic horizontal scaling script
- `load_test.py`: Performance testing and load testing tools
- `SCALING.md`: Comprehensive scaling documentation
- `Makefile`: Build automation and scaling commands

## Cleanup

```bash
docker-compose down
```
