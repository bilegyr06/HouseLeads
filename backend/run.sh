#!/bin/bash
# ============================================================================
# HomeLeads API - Startup Script (Linux/macOS)
# ============================================================================

set -e

echo "🚀 Starting HomeLeads API..."
echo ""

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  .env file not found. Please create it from .env.example"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Start the application
echo ""
echo "🎯 Starting FastAPI server on http://${HOST}:${PORT}"
echo "📖 API docs available at http://${HOST}:${PORT}/docs"
echo ""

uvicorn app.main:app --host ${HOST} --port ${PORT} --reload
