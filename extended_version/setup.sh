#!/bin/bash

# Distributed Test System Setup Script
# This script helps set up the environment and run the distributed test system

set -e

echo "🚀 Distributed Test System Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if RabbitMQ is running
check_rabbitmq() {
    print_status "Checking RabbitMQ status..."
    
    if ! command -v rabbitmqctl &> /dev/null; then
        print_warning "RabbitMQ is not installed or not in PATH"
        print_status "Please install RabbitMQ:"
        echo "  macOS: brew install rabbitmq"
        echo "  Ubuntu: sudo apt-get install rabbitmq-server"
        echo "  Windows: choco install rabbitmq"
        read -p "Press Enter after installing RabbitMQ..."
    fi
    
    # Try to check RabbitMQ status
    if rabbitmqctl status &> /dev/null; then
        print_success "RabbitMQ is running"
    else
        print_warning "RabbitMQ is not running. Starting it now..."
        
        # Try different methods to start RabbitMQ
        if command -v brew &> /dev/null; then
            brew services start rabbitmq
        elif command -v systemctl &> /dev/null; then
            sudo systemctl start rabbitmq-server
        else
            print_error "Could not start RabbitMQ automatically. Please start it manually."
            exit 1
        fi
        
        # Wait a moment and check again
        sleep 3
        if rabbitmqctl status &> /dev/null; then
            print_success "RabbitMQ started successfully"
        else
            print_error "Failed to start RabbitMQ. Please start it manually."
            exit 1
        fi
    fi
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Build Docker containers
build_containers() {
    print_status "Building Docker containers..."
    
    if docker-compose build; then
        print_success "Docker containers built successfully"
    else
        print_error "Failed to build Docker containers"
        exit 1
    fi
}

# Start worker containers
start_workers() {
    print_status "Starting worker containers..."
    
    if docker-compose up -d; then
        print_success "Worker containers started"
        
        # Wait a moment for containers to fully start
        sleep 3
        
        # Show container status
        print_status "Container status:"
        docker-compose ps
    else
        print_error "Failed to start worker containers"
        exit 1
    fi
}

# Run the dispatcher
run_dispatcher() {
    print_status "Running the dispatcher..."
    echo ""
    
    python dispatch.py
}

# Main setup process
main() {
    echo ""
    print_status "Starting setup process..."
    echo ""
    
    # Check prerequisites
    check_docker
    check_rabbitmq
    
    # Install and build
    install_dependencies
    build_containers
    
    # Start system
    start_workers
    
    echo ""
    print_success "Setup completed successfully!"
    echo ""
    print_status "You can now run the dispatcher with:"
    echo "  python dispatch.py"
    echo ""
    print_status "To stop the system:"
    echo "  docker-compose down"
    echo ""
    print_status "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
    
    # Ask if user wants to run dispatcher now
    read -p "Would you like to run the dispatcher now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        run_dispatcher
    fi
}

# Handle script arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "start")
        start_workers
        ;;
    "stop")
        print_status "Stopping worker containers..."
        docker-compose down
        print_success "Containers stopped"
        ;;
    "restart")
        print_status "Restarting worker containers..."
        docker-compose restart
        print_success "Containers restarted"
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "dispatch")
        run_dispatcher
        ;;
    "clean")
        print_status "Cleaning up containers and images..."
        docker-compose down --rmi all --volumes --remove-orphans
        print_success "Cleanup completed"
        ;;
    *)
        echo "Usage: $0 [setup|start|stop|restart|logs|dispatch|clean]"
        echo ""
        echo "Commands:"
        echo "  setup    - Full setup (default)"
        echo "  start    - Start worker containers"
        echo "  stop     - Stop worker containers"
        echo "  restart  - Restart worker containers"
        echo "  logs     - View container logs"
        echo "  dispatch - Run the dispatcher"
        echo "  clean    - Clean up all containers and images"
        exit 1
        ;;
esac
