@echo off
echo ============================================
echo Customer Insight Platform - FULL MODE Setup
echo ============================================
echo.
echo This will start the FULL mode with real web scraping.
echo You need to have Redis and Celery worker running!
echo.
echo Prerequisites:
echo   1. Redis must be running on localhost:6379
echo   2. Celery worker must be running
echo.
pause
echo.
echo [1/5] Setting DEMO_MODE=False in .env...
cd backend
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=True', 'DEMO_MODE=False' | Set-Content .env"
echo Done! Full mode enabled.
echo.
echo [2/5] Checking Redis connection...
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient('localhost', 6379); $client.Close(); Write-Host 'Redis is running!' -ForegroundColor Green } catch { Write-Host 'WARNING: Redis is NOT running!' -ForegroundColor Red; Write-Host 'Start Redis in a new terminal: redis-server' -ForegroundColor Yellow }"
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
echo.
echo IMPORTANT: Make sure Redis is running!
echo   If not, open a new terminal: redis-server
echo ============================================
echo.

cd backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
