@echo off
REM ============================================================================
REM HomeLeads API - Startup Script (Windows)
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo 🚀 Starting HomeLeads API...
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Please create it from .env.example
    pause
    exit /b 1
)

echo ✅ Environment file loaded

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run database migrations
echo 🗄️ Running database migrations...
alembic upgrade head
if !errorlevel! neq 0 (
    echo ❌ Failed to run migrations
    pause
    exit /b 1
)

REM Start the application
echo.
echo 🎯 Starting FastAPI server on http://0.0.0.0:8000
echo 📖 API docs available at http://localhost:8000/docs
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
if !errorlevel! neq 0 (
    echo ❌ Failed to start server
    pause
    exit /b 1
)

pause
