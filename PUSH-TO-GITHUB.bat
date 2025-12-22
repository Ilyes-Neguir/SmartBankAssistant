@echo off
echo ========================================
echo   Push SmartBank Assistant to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Install with default settings
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo [Step 1/6] Checking Git status...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo Initializing Git repository...
    git init
    echo Git repository initialized.
) else (
    echo Git repository already initialized.
)
echo.

echo [Step 2/6] Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Ilyes-Neguir/SmartBankAssistant.git
echo Remote added: https://github.com/Ilyes-Neguir/SmartBankAssistant.git
echo.

echo [Step 3/6] Adding all files...
git add .
echo Files staged.
echo.

echo [Step 4/6] Creating commit...
git commit -m "Complete SmartBank Assistant project

- Full-stack banking application with AI chatbot
- FastAPI backend with JWT authentication
- React frontend with TypeScript
- Complete documentation and UML diagrams
- 13 weeks of AI-First Software Engineering documentation
- Project report and presentation
- All source code and configuration files"
echo Commit created.
echo.

echo [Step 5/6] Setting main branch...
git branch -M main
echo.

echo [Step 6/6] Pushing to GitHub...
echo.
echo WARNING: You will need to authenticate!
echo.
echo If prompted for credentials:
echo   - Username: Ilyes-Neguir
echo   - Password: Use a Personal Access Token (NOT your GitHub password)
echo.
echo Generate token at: https://github.com/settings/tokens
echo Select scope: repo (full control)
echo.
echo Press any key to continue with push...
pause >nul

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo Repository: https://github.com/Ilyes-Neguir/SmartBankAssistant
    echo.
) else (
    echo.
    echo ========================================
    echo   Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Authentication failed - use Personal Access Token
    echo 2. Network connection issue
    echo 3. Repository access permissions
    echo.
    echo Try manually:
    echo   git push -u origin main
    echo.
)

pause

