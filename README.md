# Distributed Test System

A distributed automated test system built with RabbitMQ, Celery, and Docker that demonstrates task routing, worker isolation, and concurrent execution with enhanced monitoring and visualization.

## 🏗️ Architecture

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

## 🚀 Features

### Core Requirements
- ✅ **RabbitMQ Integration**: Message broker running locally
- ✅ **Celery Tasks**: Two isolated tasks (`task_a` and `task_b`)
- ✅ **Container Isolation**: Each worker processes only designated tasks
- ✅ **Concurrent Execution**: Parallel task dispatching and result collection

### Enhanced Features (Stretch Goals)
- 🎨 **Rich Visualization**: Colored output with real-time status updates
- 📊 **Performance Metrics**: Execution timing and statistics
- 📝 **Structured Logging**: JSON-formatted logs with metadata
- 🔄 **Retry Mechanism**: Automatic retries with exponential backoff
- 💾 **Result Persistence**: JSON output for further analysis
- 🐳 **Docker Orchestration**: Complete containerized deployment
- 🔍 **Health Monitoring**: Broker connection and worker status checks

## 📋 Prerequisites

- **Docker & Docker Compose**: For container orchestration
- **RabbitMQ**: Message broker (running locally, not in container)
- **Python 3.11+**: For local development and testing

## 🛠️ Setup Instructions

### 1. Install and Start RabbitMQ

#### macOS (using Homebrew)
```bash
# Install RabbitMQ
brew install rabbitmq

# Start RabbitMQ server
brew services start rabbitmq

# Or start manually
/opt/homebrew/sbin/rabbitmq-server
```

#### Ubuntu/Debian
```bash
# Install RabbitMQ
sudo apt-get update
sudo apt-get install rabbitmq-server

# Start RabbitMQ service
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
```

#### Windows
```bash
# Download and install from https://www.rabbitmq.com/download.html
# Or use Chocolatey
choco install rabbitmq

# Start RabbitMQ service
net start RabbitMQ
```

#### Verify RabbitMQ Installation
```bash
# Check if RabbitMQ is running
sudo rabbitmqctl status

# Access management UI (optional)
# http://localhost:15672 (guest/guest)
sudo rabbitmq-plugins enable rabbitmq_management
```

### 2. Clone and Setup Project

```bash
# Clone the repository (or download the files)
git clone <repository-url>
cd distributed_test_system

# Install Python dependencies (for local testing)
pip install -r requirements.txt
```

### 3. Build and Run Worker Containers

```bash
# Build the Docker image
docker-compose build

# Start both worker containers
docker-compose up -d

# Verify containers are running
docker-compose ps
```

Expected output:
```
      Name                    Command               State    Ports
----------------------------------------------------------------
celery-worker-a   celery -A celery_app worke ...   Up
celery-worker-b   celery -A celery_app worke ...   Up
```

### 4. Run the Dispatcher

```bash
# Execute the dispatcher script
python dispatch.py
```

## 📱 Expected Output

When you run `python dispatch.py`, you should see output similar to:

```
============================================================
🚀 DISTRIBUTED TASK SYSTEM DISPATCHER
============================================================
Timestamp: 2025-09-17 10:30:45
Broker: pyamqp://guest@localhost//
============================================================

✅ Broker connection successful
Active workers: 2
   • worker-a@celery-worker-a
   • worker-b@celery-worker-b

🎯 DISPATCHING TASKS CONCURRENTLY...
────────────────────────────────────────────────────────
[10:30:45.123] SENT     task_a     Dispatching task...
[10:30:45.124] SENT     task_b     Dispatching task...
[10:30:45.125] PENDING  task_a     Task ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
[10:30:45.126] PENDING  task_b     Task ID: f1e2d3c4-b5a6-7890-abcd-ef1234567890
[10:30:45.634] SUCCESS  task_a     Completed in 0.503s
[10:30:45.826] SUCCESS  task_b     Completed in 0.695s

============================================================
📊 EXECUTION RESULTS
============================================================
Total Execution Time: 0.712s
Successful Tasks: 2
Failed Tasks: 0

────────────────────────────────────────────────────────
DETAILED RESULTS
────────────────────────────────────────────────────────

✅ TASK_A
   Message: Hello from Task A
   Worker: worker-a
   Queue: queue_a
   Task ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
   Execution Time: 0.503s
   Timestamp: 2025-09-17T17:30:45.634000

✅ TASK_B
   Message: Hello from Task B
   Worker: worker-b
   Queue: queue_b
   Task ID: f1e2d3c4-b5a6-7890-abcd-ef1234567890
   Execution Time: 0.695s
   Timestamp: 2025-09-17T17:30:45.826000

────────────────────────────────────────────────────────
PERFORMANCE METRICS
────────────────────────────────────────────────────────
Average Task Time: 0.599s
Fastest Task: 0.503s
Slowest Task: 0.695s

============================================================
📄 Results saved to: dispatch_results_20250917_103045.json
🎉 Dispatch completed successfully!
```

## 🔧 Configuration

### Environment Variables

The system supports the following environment variables:

- `BROKER_URL`: RabbitMQ connection string (default: `pyamqp://guest@localhost//`)
- `WORKER_ID`: Unique identifier for each worker (set automatically in docker-compose)

### Docker Compose Configuration

The `docker-compose.yml` file configures:
- **worker-a**: Processes only `task_a` from `queue_a`
- **worker-b**: Processes only `task_b` from `queue_b`
- **Networking**: Connects to host RabbitMQ via `host.docker.internal`

## 🐛 Troubleshooting

### Common Issues

#### 1. "Connection refused" errors
```bash
# Check if RabbitMQ is running
sudo rabbitmqctl status

# Restart RabbitMQ if needed
brew services restart rabbitmq  # macOS
sudo systemctl restart rabbitmq-server  # Linux
```

#### 2. Docker containers not starting
```bash
# Check container logs
docker-compose logs worker-a
docker-compose logs worker-b

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 3. Tasks not being processed
```bash
# Verify worker queues
docker exec celery-worker-a celery -A celery_app inspect active_queues

# Check if workers are consuming
docker exec celery-worker-a celery -A celery_app inspect stats
```

#### 4. Import errors when running dispatch.py
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure celery_app.py is in the current directory
ls -la celery_app.py
```

### Debugging Commands

```bash
# View real-time logs from all containers
docker-compose logs -f

# Execute commands inside containers
docker exec -it celery-worker-a bash
docker exec -it celery-worker-b bash

# Check Celery worker status
docker exec celery-worker-a celery -A celery_app inspect stats
docker exec celery-worker-b celery -A celery_app inspect stats

# Monitor RabbitMQ queues
sudo rabbitmqctl list_queues
```

## 🧪 Testing

### Manual Testing

1. **Test individual workers**:
   ```bash
   # Start only worker-a
   docker-compose up worker-a
   
   # In another terminal, send only task_a
   python -c "from celery_app import task_a; print(task_a.delay().get())"
   ```

2. **Test task isolation**:
   ```bash
   # Start only worker-a and try to send task_b
   # It should timeout since worker-a only processes task_a
   ```

3. **Test failure scenarios**:
   ```bash
   # Stop RabbitMQ and run dispatcher
   brew services stop rabbitmq
   python dispatch.py  # Should show connection error
   ```

### Load Testing

```bash
# Create a simple load test script
cat > load_test.py << EOF
from celery_app import task_a, task_b
import time

start = time.time()
results = []

# Send 10 tasks of each type
for i in range(10):
    results.append(task_a.delay())
    results.append(task_b.delay())

# Wait for all results
for r in results:
    print(r.get())

print(f"Total time: {time.time() - start:.2f}s")
EOF

python load_test.py
```

## 📁 File Structure

```
distributed_test_system/
├── celery_app.py          # Celery configuration and tasks
├── dispatch.py            # Enhanced dispatcher with visualization
├── Dockerfile             # Container definition
├── docker-compose.yml     # Orchestration configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── dispatch_results_*.json # Generated result files
```

## 🎯 Key Implementation Details

### Task Routing
- **Queue Isolation**: Each task type routes to a specific queue
- **Worker Specialization**: Workers only consume from designated queues
- **Route Configuration**: Defined in `celery_app.py` using `task_routes`

### Structured Logging
- **JSON Format**: All logs use structured JSON with metadata
- **Task Tracking**: Each task includes ID, timing, and worker information
- **Performance Monitoring**: Execution times and retry counts tracked

### Retry Mechanism
- **Automatic Retries**: Tasks retry up to 3 times on failure
- **Exponential Backoff**: 60-second delays between retries
- **Error Handling**: Graceful degradation with detailed error reporting

### Visualization Features
- **Real-time Status**: Live updates during task execution
- **Colored Output**: Status-based color coding for better readability
- **Performance Metrics**: Detailed timing and success rate statistics
- **Result Persistence**: JSON output for further analysis

## 🚀 Stretch Goals Implemented

1. **Enhanced Visualization**: Rich colored output with real-time status updates
2. **Structured Logging**: JSON-formatted logs with comprehensive metadata
3. **Performance Monitoring**: Detailed metrics and timing information
4. **Result Persistence**: JSON output files for analysis
5. **Health Checking**: Broker and worker connectivity validation
6. **Docker Orchestration**: Complete containerized deployment with docker-compose
7. **Retry Logic**: Robust error handling with exponential backoff
8. **Concurrent Execution**: True parallel task processing with ThreadPoolExecutor

## 📝 License

This project is created for the Embedded Test Engineer Tech Challenge and demonstrates distributed system concepts using modern Python tools.

---

**Happy Testing! 🎉**
