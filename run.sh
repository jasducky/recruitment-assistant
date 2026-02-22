#!/usr/bin/env bash
#
# Startup script for the Recruitment Assistant.
# Activates the virtual environment, checks for .env, and runs main.py.
#
# Usage:
#   chmod +x run.sh
#   ./run.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Virtual environment ---
VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found at $VENV_DIR"
    echo "Create one with: python -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated: $VENV_DIR"

# --- Environment variables ---
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found"
    echo "Copy the example and add your API keys: cp .env.example .env"
    exit 1
fi

echo "Environment file found: .env"

# --- Run ---
echo "Starting Recruitment Assistant..."
echo ""
python src/main.py
