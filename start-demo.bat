@echo off
echo ======================================
echo Customer Insight Platform - Demo Mode
echo ======================================
echo.
echo [1/3] Setting DEMO_MODE=True in .env...
cd backend
powershell -Command "(Get-Content .env) -replace 'DEMO_MODE=False', 'DEMO_MODE=True' | Set-Content .env"
cd ..
echo Done! Demo mode enabled.
echo.
echo [2/3] Starting frontend in new window...
start "Frontend - React App" cmd /k "cd frontend && npm start"
echo Frontend will open at: http://localhost:3000
echo.
echo [3/3] Starting backend server...
echo Backend will run on: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the backend server
echo (Frontend will continue running in its own window)
echo ======================================
echo.

cd backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
