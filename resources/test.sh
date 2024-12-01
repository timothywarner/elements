#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <target_IP>"
    exit 1
fi

target="$1"

# Function to handle script termination
cleanup() {
    echo "Terminating script..."
    exit 0
}

# Trap interrupt signal (Ctrl+C)
trap cleanup SIGINT

while true; do
    ping -c 1 -s 65507 $target > /dev/null 2>&1
    sleep 1
done