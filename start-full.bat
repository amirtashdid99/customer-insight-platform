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
echo   2. .env file must have DEMO_MODE=False
echo.
pause
echo.
echo Starting backend server...
echo Open 2 more terminals and run:
echo   Terminal 2: redis-server
echo   Terminal 3: cd backend ^&^& venv\Scripts\activate ^&^& celery -A app.core.celery_app worker --loglevel=info --pool=solo
echo.
pause

cd backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
