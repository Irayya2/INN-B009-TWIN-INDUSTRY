@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ===========================
REM Industrial Twin - Master Launcher
REM ===========================

set "APP_DIR=C:\app"
set "BACKEND_DIR=C:\app\backend"
set "BACKEND_VENV=C:\app\backend\venv"
set "FRONTEND_DIR=C:\app\frontend"
set "LOG_DIR=C:\app\logs"

set "DB_USER=postgres"
set "DB_PASS=postgres123"
set "DB_HOST=localhost"
set "DB_PORT=5432"
set PGPASSWORD=%DB_PASS%

echo ========================================
echo Industrial Twin - One-Click Master Launcher
echo ========================================
echo.

REM ---------- PostgreSQL Check ----------
echo Checking PostgreSQL connection...
psql -U %DB_USER% -h %DB_HOST% -p %DB_PORT% -c "SELECT 1;" > "%LOG_DIR%\psql_check.log" 2>&1
if errorlevel 1 (
    echo ERROR: Cannot connect to PostgreSQL!
    echo Check %LOG_DIR%\psql_check.log for details.
    pause
    goto END
) else (
    echo PostgreSQL connection OK.
)

REM ---------- Backend .env ----------
echo.
echo Step 1: Checking backend environment...
if exist "%BACKEND_DIR%\.env" (
    echo Found backend .env
) else (
    echo Missing .env - generating from template...
    copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul
)

REM ---------- Start Backend ----------
echo.
echo Step 2: Starting Backend Server...
if not exist "%BACKEND_VENV%\Scripts\activate.bat" (
    echo ERROR: Backend venv not found at:
    echo   %BACKEND_VENV%
    echo PLEASE run:  init_database.bat
    pause
    goto END
)

start "Industrial Twin - Backend" cmd /k ^
    "cd /d %BACKEND_DIR% && call \"%BACKEND_VENV%\Scripts\activate.bat\" && python main.py"

timeout /t 4 >nul

REM ---------- Start Frontend ----------
echo.
echo Step 3: Starting Frontend Server...
start "Industrial Twin - Frontend" cmd /k ^
    "cd /d %FRONTEND_DIR% && npm install && npm run dev"

timeout /t 2 >nul

REM ---------- Sensor Generator ----------
echo.
echo Step 4: Start Sensor Generator? 
set /p SENSOR_START="Start sensor generator? (Y/N): "

if /i "%SENSOR_START%"=="Y" (
    start "Industrial Twin - Sensor Generator" cmd /k ^
        "cd /d %BACKEND_DIR%\sensors_simulation && call \"%BACKEND_VENV%\Scripts\activate.bat\" && python data_generator.py"
) else (
    echo Sensor generator skipped.
)

echo.
echo ========================================
echo ALL SERVICES STARTED SUCCESSFULLY
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
pause

:END
endlocal
