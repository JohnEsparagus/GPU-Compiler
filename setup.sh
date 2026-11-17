#!/usr/bin/env bash

# 1. Create the virtual environment if it doesn't exist yet
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 2. Activate the virtual environment (supports Linux/macOS and Git Bash on Windows)
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "Error: Could not find activation script."
    return 1 2>/dev/null || exit 1
fi

# 3. Upgrade pip and install requirements if the file exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Virtual environment is active and ready."
fi
