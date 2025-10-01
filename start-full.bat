@echo off
echo ============================================
echo Customer Insight Platform - FULL MODE Setup
echo ============================================
echo.
echo This will start the FULL mode with real web scraping.
echo.
echo Checking prerequisites...
echo.

REM Check if Redis is installed
where redis-server >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ================================================
    echo ERROR: Redis is NOT installed on your system!
    echo ================================================
    echo.
    echo You have 2 options:
    echo.
    echo Option 1: Install Redis ^(for Full Mode^)
    echo   - See REDIS_SETUP.md for installation guide
    echo   - Quick: choco install redis-64
    echo.
    echo Option 2: Use Demo Mode instead ^(recommended^)
    echo   - Run: start-demo.bat
    echo   - Works instantly, no Redis needed!
    echo.
    echo ================================================
    pause
    exit /b 1
)

echo ✅ Redis is installed.
echo.

REM Check if Redis is running
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient('localhost', 6379); $client.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ================================================
    echo ERROR: Redis is NOT running!
    echo ================================================
    echo.
    echo Please start Redis in a new terminal first:
    echo   redis-server
    echo.
    echo Then run this script again.
    echo.
    echo Alternatively, use Demo Mode:
    echo   start-demo.bat
    echo.
    echo ================================================
    pause
    exit /b 1
)

echo ✅ Redis is running on localhost:6379
echo.
echo All prerequisites met! Starting Full Mode...
echo.
pause
echo.
echo [1/5] Setting DEMO_MODE=False in .env...
cd backend
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=True', 'DEMO_MODE=False' | Set-Content .env"
echo Done! Full mode enabled.
echo.
echo [2/5] Redis connection verified ✅
echo.
echo [3/5] Starting Celery worker in new window...
cd ..
start "Celery Worker" cmd /k "cd backend && venv\Scripts\activate && celery -A app.core.celery_app worker --loglevel=info --pool=solo"
echo Celery worker started in new window.
echo.
echo [4/5] Starting frontend in new window...
start "Frontend - React App" cmd /k "cd frontend && npm start"
echo Frontend will open at: http://localhost:3000
echo.
echo [5/5] Starting backend server...
echo Backend will run on: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the backend server
echo (Frontend and Celery will continue in their windows)
echo ============================================
echo.

cd backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
