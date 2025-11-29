@echo off
REM Sensor Data Generator Startup Script
echo Starting Sensor Data Generator...
echo.

REM Move into sensor simulation folder
cd /d C:\app\backend\sensors_simulation

REM Activate correct virtual environment
call C:\app\backend\venv\Scripts\activate.bat

echo.
echo ----------------------------------------
echo  Sensor Generator Running Every 5 Seconds
echo  Press CTRL+C to stop
echo ----------------------------------------
echo.

python data_generator.py

pause




