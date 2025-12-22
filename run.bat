@echo off
setlocal enabledelayedexpansion
echo ========================================
echo   SmartBank Assistant - One-Click Run
echo ========================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker not found. Please install Docker Desktop first.
    echo Download from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM Detect Docker Compose v2 (docker compose) or v1 (docker-compose)
set "DC_CMD="
docker compose version >nul 2>&1 && set "DC_CMD=docker compose"
if not defined DC_CMD (
    docker-compose version >nul 2>&1 && set "DC_CMD=docker-compose"
)
if not defined DC_CMD (
    echo Docker Compose not found. Please enable Docker Compose V2 in Docker Desktop settings.
    pause
    exit /b 1
)

echo [1/4] Starting Docker services...
%DC_CMD% up -d postgres
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

echo [2/4] Setting up Backend...
cd backend

REM Resolve preferred Python (3.12 > py default > python)
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
    echo Download from: https://www.python.org/downloads/release/python-3120/
    cd ..
    pause
    exit /b 1
)

REM Abort early if selected Python is 3.13+ (wheels missing, triggers Rust build)
for /f "usebackq delims=" %%v in (`%PY_CMD% -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"`) do set PY_VERSION_MM=%%v
echo Detected Python version: %PY_VERSION_MM%
for /f "tokens=1,2 delims=." %%a in ("%PY_VERSION_MM%") do (
    set PY_MAJ=%%a
    set PY_MIN=%%b
)
if "%PY_MAJ%"=="3" if not "%PY_MIN%"=="12" (
    echo.
    echo Detected Python %PY_VERSION_MM%. This project currently requires Python 3.12 for prebuilt wheels.
    echo Please install Python 3.12 and re-run this script.
    echo Download: https://www.python.org/downloads/release/python-3120/
    cd ..
    pause
    exit /b 1
)

REM If venv exists but is not Python 3.12, recreate it with the selected interpreter
if exist venv (
    for /f "usebackq delims=" %%v in (`venv\Scripts\python.exe -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"`) do set VENV_PY_MM=%%v
    if not "%VENV_PY_MM%"=="3.12" (
        echo Existing virtual environment uses Python %VENV_PY_MM%. Recreating with %PY_VERSION_MM%...
        rmdir /s /q venv
    )
)

if not exist venv (
    echo Creating Python virtual environment with ^(%PY_CMD%^)...
    %PY_CMD% -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate
echo Upgrading pip/setuptools/wheel...
python -m pip install --upgrade pip setuptools wheel
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Python dependency installation failed.
    echo If you are on Python 3.13, some packages may need Rust/Cargo and MSVC.
    echo Fix by either installing Python 3.12 OR installing Rust (MSVC) and C++ Build Tools.
    echo - Rust: https://rustup.rs/
    echo - Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    cd ..
    pause
    exit /b 1
)
cd ..

echo [3/4] Setting up Frontend...
cd frontend
if not exist node_modules (
    echo Installing Node.js dependencies...
    npm install --no-fund --no-audit
)
cd ..

echo [4/4] Creating environment files...
REM Create backend .env if it doesn't exist
if not exist backend\.env (
    echo Creating backend environment file...
    (
        echo DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartbank
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo GEMINI_API_KEY=your-gemini-api-key-here
    ) > backend\.env
    echo.
    echo IMPORTANT: Please update backend\.env with your actual values:
    echo - Get Gemini API key from: https://makersuite.google.com/app/apikey
    echo - Update GEMINI_API_KEY in backend\.env
    echo.
)

REM Create frontend .env if it doesn't exist
if not exist frontend\.env (
    echo Creating frontend environment file...
    (
        echo VITE_API_URL=http://localhost:8000
        echo VITE_APP_NAME=SmartBank Assistant
    ) > frontend\.env
)

echo.
echo ========================================
echo   Starting Development Servers
echo ========================================
echo.

echo Starting Backend Server...
cd backend
start "SmartBank Backend" cmd /k "venv\Scripts\activate && python run.py"
cd ..

echo Starting Frontend Server...
cd frontend
start "SmartBank Frontend" cmd /k "npm run dev"
cd ..

echo Waiting for servers to start...
timeout /t 8 /nobreak > nul

echo.
echo ========================================
echo   SmartBank Assistant is Running!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🗄️ Database: PostgreSQL on localhost:5432
echo.
echo Opening browser...
start http://localhost:3000

echo.
echo Press any key to stop all services and exit...
pause > nul

echo.
echo Stopping services...
%DC_CMD% down
echo.
echo All services stopped. Goodbye!
