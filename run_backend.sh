#!/bin/bash
# Backend Startup Script for Linux/macOS
echo "Starting Industrial Twin Backend..."
echo

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt --quiet

# Start the server
echo
echo "Starting FastAPI server on http://localhost:8000"
echo "Press CTRL+C to stop"
echo
python main.py








