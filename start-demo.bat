@echo off
echo ======================================
echo Customer Insight Platform - Demo Mode
echo ======================================
echo.
echo Starting backend server...
echo Backend will run on: http://127.0.0.1:8000
echo.
echo NOTE: Make sure frontend is running in another terminal:
echo   cd frontend
echo   npm start
echo.
echo Press Ctrl+C to stop the server
echo ======================================
echo.

cd backend
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
