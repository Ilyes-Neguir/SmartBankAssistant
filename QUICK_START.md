# 🚀 Quick Start - SmartBank Assistant

## One-Click Run

### Option 1: Windows Batch File (Recommended)
```bash
run.bat
```

### Option 2: PowerShell (Alternative)
```powershell
.\run.ps1
```

### Option 3: Manual Setup
```bash
# 1. Start database
docker-compose up -d postgres

# 2. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 3. Setup frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## What the Run Script Does

1. **Checks Docker** - Ensures Docker Desktop is installed
2. **Starts Database** - Launches PostgreSQL in Docker
3. **Sets up Backend** - Creates virtual environment and installs dependencies
4. **Sets up Frontend** - Installs Node.js dependencies
5. **Creates Config Files** - Generates `.env` files with default values
6. **Starts Servers** - Launches both backend and frontend
7. **Opens Browser** - Automatically opens http://localhost:3000

## Prerequisites

- **Docker Desktop** - Download from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Python 3.8+** - For backend
- **Node.js 18+** - For frontend

## Configuration

After first run, update these files:

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smartbank
SECRET_KEY=your-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key-here  # Get from https://makersuite.google.com/app/apikey
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=SmartBank Assistant
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on localhost:5432

## Troubleshooting

### Docker Issues
- Make sure Docker Desktop is running
- Check if ports 3000, 8000, 5432 are available

### Python Issues
- Ensure Python 3.8+ is installed
- Check if virtual environment is created properly

### Node.js Issues
- Ensure Node.js 18+ is installed
- Clear npm cache: `npm cache clean --force`

### Database Issues
- Check if PostgreSQL container is running: `docker ps`
- Reset database: `docker-compose down -v && docker-compose up -d postgres`

## Stopping the Application

- Press any key in the terminal to stop all services
- Or manually stop: `docker-compose down`
