#!/bin/bash
# CTFd Setup Script
# Run this on your home PC to set up CTFd

set -e

echo "=========================================="
echo "CTFd Setup for College CTF"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        echo "Docker installed. Please log out and log back in for group changes to take effect."
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
        exit 1
    else
        echo "Unsupported OS. Please install Docker manually."
        exit 1
    fi
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Installing..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p CTFd/uploads CTFd/logs data/db

# Generate a random secret key
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/your-secret-key-change-this/$SECRET_KEY/" docker-compose.yml

# Start CTFd
echo "Starting CTFd..."
docker-compose up -d

echo ""
echo "=========================================="
echo "CTFd is starting up!"
echo "=========================================="
echo ""
echo "Access CTFd at: http://localhost:8000"
echo ""
echo "First-time setup:"
echo "1. Open http://localhost:8000 in your browser"
echo "2. Follow the setup wizard"
echo "3. Create admin account"
echo "4. Import challenges using the import script"
echo ""
echo "To stop CTFd: docker-compose down"
echo "To view logs: docker-compose logs -f"
echo ""
