#!/bin/bash
# Master Launch Script - Starts all web challenges
# Usage: ./launch_web_challenges.sh [start|stop|status]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_DIR="$SCRIPT_DIR/.pids"
LOG_DIR="$SCRIPT_DIR/logs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Challenge definitions: name|port|directory
CHALLENGES=(
    "Cookie Monster|5002|easy/05_cookie_monster"
    "SQL Rookie|5003|easy/10_sql_rookie"
    "Broken Auth|5004|medium/12_broken_auth"
    "Path Traversal|5005|medium/14_path_traversal"
    "XSS Reflected|5006|medium/15_xss_reflected"
    "IDOR|5007|medium/18_idor"
    "SSRF Master|5008|hard/21_ssrf_master"
    "Padding Oracle|5009|hard/22_padding_oracle"
)

mkdir -p "$PID_DIR" "$LOG_DIR"

start_challenge() {
    local name="$1"
    local port="$2"
    local dir="$3"
    local pid_file="$PID_DIR/${name// /_}.pid"
    local log_file="$LOG_DIR/${name// /_}.log"
    
    # Check if already running
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${YELLOW}[SKIP]${NC} $name already running (PID: $pid, Port: $port)"
            return
        fi
    fi
    
    # Check if port is in use
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}[ERROR]${NC} Port $port already in use for $name"
        return
    fi
    
    echo -e "${BLUE}[START]${NC} Starting $name on port $port..."
    
    cd "$SCRIPT_DIR/$dir"
    nohup python3 app.py > "$log_file" 2>&1 &
    local pid=$!
    echo $pid > "$pid_file"
    
    # Wait a moment and check if it started
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
        echo -e "${GREEN}[OK]${NC} $name started (PID: $pid, Port: $port)"
    else
        echo -e "${RED}[FAIL]${NC} $name failed to start. Check logs: $log_file"
        rm -f "$pid_file"
    fi
}

stop_challenge() {
    local name="$1"
    local pid_file="$PID_DIR/${name// /_}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            echo -e "${RED}[STOP]${NC} Stopped $name (PID: $pid)"
        fi
        rm -f "$pid_file"
    fi
}

status_challenge() {
    local name="$1"
    local port="$2"
    local pid_file="$PID_DIR/${name// /_}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}[RUNNING]${NC} $name (PID: $pid, Port: $port)"
            return
        fi
    fi
    echo -e "${RED}[STOPPED]${NC} $name (Port: $port)"
}

start_all() {
    echo "=========================================="
    echo "  Starting All Web Challenges"
    echo "=========================================="
    echo ""
    
    for challenge in "${CHALLENGES[@]}"; do
        IFS='|' read -r name port dir <<< "$challenge"
        start_challenge "$name" "$port" "$dir"
    done
    
    echo ""
    echo "=========================================="
    echo "  All challenges started!"
    echo "=========================================="
    echo ""
    show_urls
}

stop_all() {
    echo "=========================================="
    echo "  Stopping All Web Challenges"
    echo "=========================================="
    echo ""
    
    for challenge in "${CHALLENGES[@]}"; do
        IFS='|' read -r name port dir <<< "$challenge"
        stop_challenge "$name" "$port" "$dir"
    done
    
    # Clean up
    rm -rf "$PID_DIR"
    echo ""
    echo "All challenges stopped."
}

status_all() {
    echo "=========================================="
    echo "  Challenge Status"
    echo "=========================================="
    echo ""
    
    for challenge in "${CHALLENGES[@]}"; do
        IFS='|' read -r name port dir <<< "$challenge"
        status_challenge "$name" "$port"
    done
}

show_urls() {
    echo "Challenge URLs:"
    echo "----------------------------------------"
    for challenge in "${CHALLENGES[@]}"; do
        IFS='|' read -r name port dir <<< "$challenge"
        printf "  %-20s http://localhost:%s\n" "$name" "$port"
    done
    echo ""
}

restart_all() {
    stop_all
    sleep 2
    start_all
}

case "${1:-start}" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    status)
        status_all
        ;;
    restart)
        restart_all
        ;;
    urls)
        show_urls
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|urls}"
        exit 1
        ;;
esac
