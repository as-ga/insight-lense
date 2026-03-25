#!/bin/bash

# Backend startup script using environment variables

cd "$(dirname "$0")/backend"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Run FastAPI with environment variables
echo "🚀 Starting Analytics Backend..."
echo "📍 Host: $API_HOST"
echo "🔌 Port: $API_PORT"
echo "🌍 Environment: $FLASK_ENV"

python -m uvicorn app.main:app --host $API_HOST --port $API_PORT --reload
