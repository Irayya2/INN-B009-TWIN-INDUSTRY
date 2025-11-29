#!/bin/bash
# Database Initialization Script for Linux/macOS
echo "Initializing Industrial Twin Database..."
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
pip install -r requirements.txt --quiet

# Run initialization script
cd ..
echo
echo "Running database initialization..."
python3 scripts/init_db.py

echo
echo "Database initialization complete!"








