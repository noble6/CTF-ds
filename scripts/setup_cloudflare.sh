#!/bin/bash
# Cloudflare Tunnel Setup Script
# Makes your local CTFd accessible on the internet for FREE

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         CLOUDFLARE TUNNEL SETUP                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}cloudflared not found. Installing...${NC}"
    
    # Detect architecture
    ARCH=$(uname -m)
    case $ARCH in
        x86_64)
            ARCH="amd64"
            ;;
        aarch64|arm64)
            ARCH="arm64"
            ;;
        *)
            echo -e "${RED}Unsupported architecture: $ARCH${NC}"
            exit 1
            ;;
    esac
    
    # Download cloudflared
    curl -L "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${ARCH}" -o cloudflared
    chmod +x cloudflared
    
    echo -e "${GREEN}✓ cloudflared installed${NC}"
fi

echo -e "${BLUE}Starting Cloudflare Tunnel...${NC}"
echo ""
echo "This will create a public URL for your local CTFd instance."
echo "Anyone on the internet will be able to access it."
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the tunnel${NC}"
echo ""
echo "=========================================="
echo ""

# Start tunnel
./cloudflared tunnel --url http://localhost:8000

