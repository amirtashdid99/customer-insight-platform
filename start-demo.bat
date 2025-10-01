@echo off
echo ======================================
echo Customer Insight Platform - Demo Mode
echo ======================================
echo.
echo [1/2] Setting DEMO_MODE=True in .env...
cd backend
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=False', 'DEMO_MODE=True' | Set-Content .env"
echo Done! Demo mode enabled.
echo.
echo [2/2] Starting backend server...
echo Backend will run on: http://127.0.0.1:8000
echo.
echo NOTE: Make sure frontend is running in another terminal:
echo   cd frontend
echo   npm start
echo.
echo Press Ctrl+C to stop the server
echo ======================================
echo.

call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
