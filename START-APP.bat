@echo off
echo ========================================
echo   Starting SmartBank Assistant
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "Backend - SmartBank" cmd /k "cd /d ""%~dp0backend"" && venv\Scripts\python.exe run.py"

echo [2/2] Starting Frontend Server...
timeout /t 2 /nobreak >nul
start "Frontend - SmartBank" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Waiting for servers to start...
timeout /t 8 /nobreak >nul

echo Opening browser...
start http://localhost:3000

echo.
echo Done! Check the two windows that opened.
echo.
pause

