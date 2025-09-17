# Distributed Test System

A distributed automated test system built with RabbitMQ, Celery, and Docker that demonstrates task routing, worker isolation, and concurrent execution.

## 🎯 **Two Complete Implementations**

This repository provides **two complete versions** of the distributed test system:

### 📦 **[Minimal Version](./minimal_version/)** - Bare Essentials
- ✅ **Core requirements only** - Just what's needed to pass the challenge
- 📝 **~60 lines of code** across 5 files
- 🚀 **Quick setup** - Get running in minutes
- 🎓 **Perfect for learning** - Understand the fundamentals
- 💡 **Simple output**: `Result from task_a: Hello from Task A`

### 🚀 **[Extended Version](./extended_version/)** - Production Ready
- ✅ **All core requirements** + advanced features
- 📝 **1200+ lines of code** with comprehensive implementation
- 🎨 **Rich visualization** - Colored output with real-time monitoring
- 📊 **Performance metrics** - Detailed timing and statistics
- 🔧 **Production features** - Logging, health checks, automation
- 💼 **Enterprise ready** - Structured logging, error handling, retry logic

📊 **[View Detailed Comparison](./COMPARISON.md)** - Side-by-side feature analysis of both versions

---

## 🚀 **Quick Start**

### 🎯 **Minimal Version** (Learning & Prototyping)
```bash
cd minimal_version
pip install -r requirements.txt
docker-compose up -d
python dispatch.py
```

### 🚀 **Extended Version** (Production Ready)
```bash
cd extended_version
./setup.sh  # Automated setup
# or manual: pip install -r requirements.txt && docker-compose up -d && python dispatch.py
```

---

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


## 🐛 Troubleshooting

### Common Issues

#### 1. "Connection refused" errors
```bash
# Check if RabbitMQ is running
sudo rabbitmqctl status

# Start RabbitMQ if needed
brew services start rabbitmq  # macOS
sudo systemctl start rabbitmq-server  # Linux
```

#### 2. Docker containers not starting
```bash
# Check container logs
docker-compose logs worker-a
docker-compose logs worker-b

# Rebuild containers if needed
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 3. Import errors when running dispatch.py
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure you're in the correct directory
ls -la celery_app.py  # Should exist
```

#### 4. Tasks not being processed
```bash
# Check if workers are consuming from correct queues
docker-compose ps  # Should show both workers running

# Monitor RabbitMQ queues
sudo rabbitmqctl list_queues
```

## ⚙️ Configuration

The system uses environment variables for configuration:

- **`BROKER_URL`**: RabbitMQ connection string (default: `pyamqp://guest@localhost//`)
- **`WORKER_ID`**: Unique identifier for each worker (set automatically in docker-compose)

## 🧪 Testing

### Quick Test
```bash
# Test both versions work
cd minimal_version && python dispatch.py
cd ../extended_version && python dispatch.py
```

### Load Testing (Extended Version)
```bash
cd extended_version
python -c "
from celery_app import task_a, task_b
import time

start = time.time()
results = [task_a.delay() for _ in range(5)] + [task_b.delay() for _ in range(5)]
for r in results: print(r.get())
print(f'Total time: {time.time() - start:.2f}s')
"
```

## 🔧 Need More Help?

- **Detailed Setup Instructions**: See version-specific README files
- **Feature Comparison**: Review [COMPARISON.md](./COMPARISON.md) for detailed analysis


## 📁 Repository Structure

```
distributed-test-system/
├── 📁 minimal_version/              # Bare essentials implementation
│   ├── celery_app.py               # Basic Celery config (20 lines)
│   ├── dispatch.py                 # Simple dispatcher (15 lines)
│   ├── Dockerfile                  # Basic container (8 lines)
│   ├── docker-compose.yml          # Simple orchestration (10 lines)
│   ├── requirements.txt            # Just celery (1 line)
│   └── README.md                   # Minimal setup guide
├── 📁 extended_version/             # Production-ready implementation
│   ├── celery_app.py               # Advanced config + logging (165 lines)
│   ├── dispatch.py                 # Rich visualization (250 lines)
│   ├── Dockerfile                  # Hardened container (30 lines)
│   ├── docker-compose.yml          # Full orchestration (49 lines)
│   ├── requirements.txt            # Multiple dependencies (4 lines)
│   ├── setup.sh                    # Automated setup (224 lines)
│   ├── test-config.yml             # Configuration options (72 lines)
│   └── README.md                   # Comprehensive guide
├── COMPARISON.md                    # Detailed comparison of both versions
└── README.md                       # This file - overview of both versions
```


## 📝 License

This project is created for the Embedded Test Engineer Tech Challenge and demonstrates distributed system concepts using modern Python tools.

---

**Happy Testing! 🎉**
