#!/bin/bash

# Property Comparison App Startup Script

echo "🏠 Starting Property Comparison App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use. Please free the port and try again."
        exit 1
    fi
}

# Check if required ports are available
echo "🔍 Checking ports..."
check_port 8000
check_port 3000

# Start backend
echo "🚀 Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -q -r requirements.txt

# Start backend in background
echo "🔧 Starting FastAPI server on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../frontend

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install --silent

# Start frontend
echo "🔧 Starting React app on http://localhost:3000"
npm start &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 5

echo ""
echo "✅ Property Comparison App is running!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT

# Wait for processes
wait