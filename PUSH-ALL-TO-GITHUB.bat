@echo off
echo ========================================
echo   Pushing to GitHub Repository
echo ========================================
echo.

REM Configure Git identity
echo [1/7] Configuring Git identity...
git config user.email "ilyes.neguir@example.com"
git config user.name "Ilyes Neguir"
echo Done.
echo.

REM Initialize repository if needed
echo [2/7] Checking Git repository...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo Initializing Git repository...
    git init
)
echo Done.
echo.

REM Add remote
echo [3/7] Configuring remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Ilyes-Neguir/SmartBankAssistant.git
echo Remote: https://github.com/Ilyes-Neguir/SmartBankAssistant.git
echo Done.
echo.

REM Add all files
echo [4/7] Adding all files...
git add .
echo Done.
echo.

REM Commit
echo [5/7] Creating commit...
git commit -m "Complete SmartBank Assistant project - Full-stack banking app with AI chatbot, documentation, presentation, and UML diagrams"
if %errorlevel% neq 0 (
    echo ERROR: Commit failed!
    echo Make sure you configured Git identity:
    echo   git config user.email "your-email@example.com"
    echo   git config user.name "Your Name"
    pause
    exit /b 1
)
echo Done.
echo.

REM Set branch to main
echo [6/7] Setting branch to main...
git branch -M main
echo Done.
echo.

REM Push to GitHub
echo [7/7] Pushing to GitHub...
echo.
echo WARNING: You will need to authenticate!
echo Use your GitHub Personal Access Token as password.
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! All files pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/Ilyes-Neguir/SmartBankAssistant
    echo.
    start https://github.com/Ilyes-Neguir/SmartBankAssistant
) else (
    echo.
    echo ========================================
    echo   Push failed!
    echo ========================================
    echo.
    echo Make sure you:
    echo 1. Have a Personal Access Token (not password)
    echo 2. Token has 'repo' scope enabled
    echo 3. Repository exists on GitHub
    echo.
)

pause

