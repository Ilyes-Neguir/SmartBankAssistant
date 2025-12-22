@echo off
setlocal enabledelayedexpansion
echo Setting up SmartBank Assistant...

echo.
echo ========================================
echo   SmartBank Assistant - Setup
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend
REM Pick preferred Python
set "PY_CMD="
py -3.12 -V >nul 2>&1 && set "PY_CMD=py -3.12"
if not defined PY_CMD (
    py -V >nul 2>&1 && set "PY_CMD=py"
)
if not defined PY_CMD (
    python -V >nul 2>&1 && set "PY_CMD=python"
)
if not defined PY_CMD (
    echo Python not found. Please install Python 3.12 and add it to PATH.
    echo Download: https://www.python.org/downloads/release/python-3120/
    cd ..
    pause
    exit /b 1
)

for /f "usebackq delims=" %%v in (`%PY_CMD% -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"`) do set PY_VERSION_MM=%%v
echo Using Python %PY_VERSION_MM%
for /f "tokens=1,2 delims=." %%a in ("%PY_VERSION_MM%") do (
    set PY_MAJ=%%a
    set PY_MIN=%%b
)
if not "%PY_MAJ%.%PY_MIN%"=="3.12" (
    echo This project requires Python 3.12. Please install it and re-run setup.
    cd ..
    pause
    exit /b 1
)

if exist venv (
    for /f "usebackq delims=" %%v in (`venv\Scripts\python.exe -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"`) do set VENV_PY_MM=%%v
    if not "%VENV_PY_MM%"=="3.12" (
        echo Existing venv uses Python %VENV_PY_MM%. Recreating with %PY_VERSION_MM%...
        rmdir /s /q venv
    )
)

if not exist venv (
    echo Creating virtual environment...
    %PY_CMD% -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate
echo Upgrading pip/setuptools/wheel...
python -m pip install --upgrade pip setuptools wheel
echo Installing Python dependencies...
pip install -r requirements.txt
cd ..

echo [2/4] Setting up Frontend...
cd frontend
echo Installing Node.js dependencies...
npm install --no-fund --no-audit
cd ..

echo [3/4] Creating configuration files...
if not exist backend\.env (
    (
        echo DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartbank
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo GEMINI_API_KEY=your-gemini-api-key-here
    ) > backend\.env
)
if not exist frontend\.env (
    (
        echo VITE_API_URL=http://localhost:8000
        echo VITE_APP_NAME=SmartBank Assistant
    ) > frontend\.env
)

echo [4/4] Setup complete!
echo.
echo ========================================
echo   Setup Instructions
echo ========================================
echo.
echo 1. Configure your database:
echo    - Create PostgreSQL database named 'smartbank'
echo    - Update DATABASE_URL in backend/.env
echo.
echo 2. Configure Gemini AI:
echo    - Get API key from Google AI Studio
echo    - Update GEMINI_API_KEY in backend/.env
echo.
echo 3. Initialize database:
echo    - Run: cd backend && python run.py
echo.
echo 4. Start development:
echo    - Run: start-dev.bat
echo.
echo Press any key to exit...
pause > nul
