# SmartBank Assistant - One-Click Run (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SmartBank Assistant - One-Click Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is available
try {
    docker --version | Out-Null
    Write-Host "✓ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Detect Docker Compose v2 or v1
$useDockerCompose = $false
try { 
    docker compose version | Out-Null
    $useDockerCompose = $true
    Write-Host "Using Docker Compose V2" -ForegroundColor Gray
} catch {
    try { 
        docker-compose version | Out-Null
        $useDockerCompose = $false
        Write-Host "Using Docker Compose V1" -ForegroundColor Gray
    } catch {
        Write-Host "❌ Docker Compose not found. Enable Docker Compose V2 in Docker Desktop settings." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "[1/4] Starting Docker services..." -ForegroundColor Yellow
if ($useDockerCompose) {
    docker compose up -d postgres
} else {
    docker-compose up -d postgres
}
Write-Host "Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "[2/4] Setting up Backend..." -ForegroundColor Yellow
Set-Location backend

# Prefer Python 3.8 or later
$py = "python"
try { 
    $null = python --version 2>&1
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ and add to PATH." -ForegroundColor Red
    Read-Host "Press Enter to exit" | Out-Null
    exit 1
}

$pyVer = (python -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')").Trim()
Write-Host "Detected Python version: $pyVer" -ForegroundColor Yellow
$pyMajor = [int]($pyVer.Split('.')[0])
$pyMinor = [int]($pyVer.Split('.')[1])
if ($pyMajor -lt 3 -or ($pyMajor -eq 3 -and $pyMinor -lt 8)) {
    Write-Host "❌ Python 3.8+ required. Current version: $pyVer" -ForegroundColor Red
    Set-Location ..
    Read-Host "Press Enter to exit" | Out-Null
    exit 1
}

if (Test-Path "venv") {
    try {
        $venvVer = (& "venv\Scripts\python.exe" -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')").Trim()
        $venvMajor = [int]($venvVer.Split('.')[0])
        $venvMinor = [int]($venvVer.Split('.')[1])
    } catch { $venvVer = ""; $venvMajor = 0; $venvMinor = 0 }
    if ($venvMajor -lt 3 -or ($venvMajor -eq 3 -and $venvMinor -lt 8) -or $venvVer -ne $pyVer) {
        Write-Host "Recreating virtual environment with Python $pyVer..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
    }
}

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "Upgrading pip/setuptools/wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Set-Location ..

Write-Host "[3/4] Setting up Frontend..." -ForegroundColor Yellow
Set-Location frontend
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
}
Set-Location ..

Write-Host "[4/4] Creating environment files..." -ForegroundColor Yellow
# Create backend .env if it doesn't exist
if (-not (Test-Path "backend\.env")) {
    Write-Host "Creating backend environment file..." -ForegroundColor Yellow
    @"
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartbank
SECRET_KEY=your-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key-here
"@ | Out-File -FilePath "backend\.env" -Encoding UTF8
    Write-Host ""
    Write-Host "IMPORTANT: Please update backend\.env with your actual values:" -ForegroundColor Red
    Write-Host "- Get Gemini API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    Write-Host "- Update GEMINI_API_KEY in backend\.env" -ForegroundColor Yellow
    Write-Host ""
}

# Create frontend .env if it doesn't exist
if (-not (Test-Path "frontend\.env")) {
    Write-Host "Creating frontend environment file..." -ForegroundColor Yellow
    @"
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=SmartBank Assistant
"@ | Out-File -FilePath "frontend\.env" -Encoding UTF8
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Development Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Set-Location backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "venv\Scripts\Activate.ps1; python run.py"
Set-Location ..

Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Set-Location frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
Set-Location ..

Write-Host "Waiting for servers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SmartBank Assistant is Running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️ Database: PostgreSQL on localhost:5432" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Press any key to stop all services and exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Stopping services..." -ForegroundColor Yellow
if ($useDockerCompose) {
    docker compose down
} else {
    docker-compose down
}
Write-Host ""
Write-Host "All services stopped. Goodbye!" -ForegroundColor Green
