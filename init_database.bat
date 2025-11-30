@echo off
REM Database Initialization Script for Windows
echo Initializing Industrial Twin Database...
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
pip install -r requirements.txt --quiet

REM Run initialization script
cd ..
echo.
echo Running database initialization...
python scripts/init_db.py

echo.
echo Database initialization complete!
pause










