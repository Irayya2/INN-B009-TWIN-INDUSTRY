@echo off
set PGPASSWORD=postgres123

REM Complete Startup Script - Starts all services
echo ========================================
echo Industrial Twin System - Complete Startup
echo ========================================
echo.

REM Check if PostgreSQL is running (basic check)
echo Checking PostgreSQL connection...
psql -U postgres -h localhost -c "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot connect to PostgreSQL!
    echo Please ensure PostgreSQL is running and credentials are correct.
    echo.
) else (
    echo PostgreSQL connection OK!
)

REM Step 1: Initialize Database (if not done)
echo.
echo Step 1: Checking database...
if exist "backend\.env" (
    echo Database configuration found.
) else (
    echo Creating .env file from template...
    copy backend\.env.example backend\.env >nul 2>&1
    echo.
    echo PLEASE EDIT backend\.env with your database credentials!
    echo.
    pause
)

REM Step 2: Start Backend
echo.
echo Step 2: Starting Backend Server...
echo Opening new window for backend...
start "Industrial Twin - Backend" cmd /k "call C:\app\backend\venv\Scripts\activate.bat && python backend\main.py"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Step 3: Start Frontend
echo.
echo Step 3: Starting Frontend Server...
echo Opening new window for frontend...
start "Industrial Twin - Frontend" cmd /k "cd frontend && npm install && npm run dev"

REM Step 4: Sensor Data Generator
echo.
echo Step 4: Sensor Data Generator (Optional)
set /p start_sensor="Start sensor data generator? (Y/N): "
if /i "%start_sensor%"=="Y" (
    start "Industrial Twin - Sensor Generator" cmd /k "run_sensor_generator.bat"
)

echo.
echo ========================================
echo All services starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
pause




