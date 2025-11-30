#!/bin/bash
# Sensor Data Generator Startup Script for Linux/macOS
echo "Starting Sensor Data Generator..."
echo

cd backend/sensors_simulation

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Virtual environment not found. Please run init_database.sh first!"
    exit 1
fi

# Activate virtual environment
source ../venv/bin/activate

# Start the generator
echo
echo "Generating sensor data every 5 seconds..."
echo "Press CTRL+C to stop"
echo
python data_generator.py










