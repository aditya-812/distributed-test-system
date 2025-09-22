# DevContainer Setup

Minimal VS Code development container.

## Quick Start

1. **Start RabbitMQ on host**:
   ```bash
   brew services start rabbitmq  # macOS
   ```

2. **Open in VS Code**:
   ```bash
   code .
   ```

3. **Reopen in Container**:
   - `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

4. **Use the system**:
   ```bash
   make up    # Start workers
   make run   # Run dispatcher  
   ```

## What it provides

- Python 3.11 environment
- Python VS Code extension
- Access to existing Makefile commands

That's it!