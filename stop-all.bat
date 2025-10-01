@echo off
echo ==========================================
echo Stopping Customer Insight Platform
echo ==========================================
echo.

echo Stopping backend (uvicorn)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
if %errorlevel% == 0 (
    echo   Backend stopped.
) else (
    echo   No backend process found.
)

echo.
echo Stopping frontend (React)...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *Frontend*" 2>nul
if %errorlevel% == 0 (
    echo   Frontend stopped.
) else (
    echo   No frontend process found.
)

echo.
echo Stopping Celery worker...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Celery*" 2>nul
if %errorlevel% == 0 (
    echo   Celery stopped.
) else (
    echo   No Celery process found.
)

echo.
echo ==========================================
echo All processes stopped!
echo ==========================================
echo.
pause
