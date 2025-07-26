#!/bin/bash

# Shell wrapper for Apple Notes MCP Server
# This ensures Python is found correctly in the DXT runtime environment

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find Python in common locations
PYTHON_CMD=""

# Check for python3 first (most common)
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
elif [ -f "/usr/bin/python3" ]; then
    PYTHON_CMD="/usr/bin/python3"
elif [ -f "/opt/homebrew/bin/python3" ]; then
    PYTHON_CMD="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PYTHON_CMD="/usr/local/bin/python3"
else
    echo "Error: Python not found. Please ensure Python 3.13+ is installed." >&2
    exit 1
fi

# Execute the main.py script with the found Python
exec "$PYTHON_CMD" "$SCRIPT_DIR/main.py" "$@"