#!/bin/bash

# Complete startup script for full stack

echo "🚀 Starting Insight Lense Dashboard..."

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    exit 1
fi

# Start backend in background
echo "📍 Starting backend on port 8000..."
cd backend
export $(cat .env | grep -v '#' | xargs)
python -m uvicorn app.main:app --host $API_HOST --port $API_PORT --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "🎨 Starting frontend on port 5173..."
cd frontend
pnpm dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both services started!"
echo "📊 Dashboard: http://localhost:5173"
echo "🔌 API: http://localhost:8000"
echo "❤️  Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
