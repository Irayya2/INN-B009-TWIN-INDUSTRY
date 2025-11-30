@echo off
REM Clean & Proper Backend Startup Script
echo Starting Industrial Twin Backend...
echo.

REM Move into backend folder
cd /d C:\app\backend

REM Activate correct virtual environment
call C:\app\backend\venv\Scripts\activate.bat

REM Start API server
echo.
echo ----------------------------------------
echo  Industrial Twin Backend is starting...
echo  URL: http://localhost:8000
echo ----------------------------------------
echo.

python main.py

pause






