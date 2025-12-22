@echo off
setlocal
echo Starting SmartBank Assistant Development Environment...

echo.
echo ========================================
echo   SmartBank Assistant - Development
echo ========================================
echo.

REM Ensure backend venv exists and is ready
if not exist backend\venv (
    echo Backend virtual environment not found. Running initial setup...
    call run.bat
    goto :end
)

echo [1/3] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "venv\Scripts\activate && python run.py"
cd ..

echo [2/3] Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "npm run dev"
cd ..

echo [3/3] Opening Browser...
timeout /t 5 /nobreak > nul
start http://localhost:3000

echo.
echo ========================================
echo   Development servers started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul

:end
