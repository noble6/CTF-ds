#!/bin/bash
# Quick Start Script - Sets up everything in one command
# Usage: ./quickstart.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         COLLEGE CTF 2026 - QUICK START SETUP             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Step 1: Check dependencies
echo -e "${BLUE}[1/5]${NC} Checking dependencies..."

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 found${NC}"
        return 0
    fi
}

MISSING=0
check_command python3 || MISSING=1
check_command pip3 || MISSING=1
check_command docker || MISSING=1

if [ $MISSING -eq 1 ]; then
    echo -e "${YELLOW}Some dependencies missing. Installing...${NC}"
    
    # Try to install Python packages
    if command -v pip3 &> /dev/null; then
        echo "Installing Python packages..."
        pip3 install -r requirements.txt --quiet
    fi
fi

# Step 2: Install Python dependencies
echo ""
echo -e "${BLUE}[2/5]${NC} Installing Python dependencies..."
pip3 install -r requirements.txt --quiet 2>/dev/null || {
    echo -e "${YELLOW}Warning: Some packages may need manual installation${NC}"
    echo "Run: pip3 install -r requirements.txt"
}

# Step 3: Generate challenge files
echo ""
echo -e "${BLUE}[3/5]${NC} Generating challenge files..."
cd scripts
python3 generate_all.py
cd ..

# Step 4: Verify challenges
echo ""
echo -e "${BLUE}[4/5]${NC} Verifying challenges..."
cd scripts
python3 verify_challenges.py --quick
cd ..

# Step 5: Start CTFd
echo ""
echo -e "${BLUE}[5/5]${NC} Starting CTFd..."
cd ctfd_setup

# Check if Docker is running
if docker info &> /dev/null; then
    echo "Starting CTFd with Docker..."
    docker-compose up -d 2>/dev/null || {
        echo -e "${YELLOW}Docker Compose failed. Trying alternative...${NC}"
        echo "Please start CTFd manually:"
        echo "  cd ctfd_setup && docker-compose up -d"
    }
else
    echo -e "${YELLOW}Docker not running. Please start Docker and run:${NC}"
    echo "  cd ctfd_setup && docker-compose up -d"
fi

cd ..

# Final instructions
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                    SETUP COMPLETE!                        ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo ""
echo "  1. Wait 30 seconds for CTFd to start"
echo "  2. Open http://localhost:8000 in your browser"
echo "  3. Complete CTFd setup wizard"
echo "  4. Get API token from: Admin → Config → API"
echo "  5. Import challenges:"
echo ""
echo -e "     ${CYAN}cd scripts${NC}"
echo -e "     ${CYAN}python3 import_challenges.py --url http://localhost:8000 --token YOUR_TOKEN${NC}"
echo ""
echo "  6. Start web challenges:"
echo ""
echo -e "     ${CYAN}./scripts/launch_web_challenges.sh start${NC}"
echo ""
echo "  7. Make public (optional):"
echo ""
echo -e "     ${CYAN}./cloudflared tunnel --url http://localhost:8000${NC}"
echo ""
echo -e "${YELLOW}Documentation: See README.md for full instructions${NC}"
echo ""
