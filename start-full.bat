@echo off
echo ============================================
echo Customer Insight Platform - FULL MODE Setup
echo ============================================
echo.
echo This will start the FULL mode with real web scraping.
echo You need to have Redis running first!
echo.
echo Prerequisites:
echo   1. Redis must be running on localhost:6379
echo   2. Celery worker must be running
echo.
pause
echo.
echo [1/3] Setting DEMO_MODE=False in .env...
cd backend
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=True', 'DEMO_MODE=False' | Set-Content .env"
echo Done! Full mode enabled.
echo.
echo [2/3] Checking Redis connection...
powershell -Command "try { $client = New-Object System.Net.Sockets.TcpClient('localhost', 6379); $client.Close(); Write-Host 'Redis is running!' -ForegroundColor Green } catch { Write-Host 'WARNING: Redis is NOT running!' -ForegroundColor Red; Write-Host 'Start Redis first: redis-server' -ForegroundColor Yellow }"
echo.
echo [3/3] Starting backend server...
echo.
echo IMPORTANT: Open 2 more terminals and run:
echo   Terminal 2: redis-server
echo   Terminal 3: cd backend ^&^& venv\Scripts\activate ^&^& celery -A app.core.celery_app worker --loglevel=info --pool=solo
echo.
pause

call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
