@echo off
echo 🚀 Roommate Match - Deployment Script
echo ====================================
echo.

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Railway CLI...
    npm install -g @railway/cli
)

REM Login to Railway
echo 🔐 Logging into Railway...
railway login

REM Navigate to backend directory
cd backend

REM Initialize Railway project
echo 🚂 Initializing Railway project...
railway init --name "roommate-match"

REM Deploy
echo 📤 Deploying to Railway...
railway up

echo.
echo 🔑 Please set your OpenAI API key:
echo railway variables set OPENAI_API_KEY=your_openai_api_key_here
echo.
echo 📋 Get your API key from: https://platform.openai.com/api-keys
echo.
echo 🌐 Your app will be available at the URL shown above once deployment completes!
pause