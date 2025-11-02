#!/bin/bash

# Setup script for Property Comparison App

echo "🏠 Setting up Property Comparison App..."
echo ""

# Check system requirements
echo "🔍 Checking system requirements..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.8+ from https://python.org"
    exit 1
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required. Please install Node.js 16+ from https://nodejs.org"
    exit 1
else
    echo "✅ Node.js found: $(node --version)"
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required (usually comes with Node.js)"
    exit 1
else
    echo "✅ npm found: $(npm --version)"
fi

echo ""
echo "📦 Installing dependencies..."

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "  📦 Installing Python packages..."
pip install -q -r requirements.txt

echo "  ✅ Backend setup complete!"

# Setup frontend
echo "🎨 Setting up frontend..."
cd ../frontend

# Install Node dependencies
echo "  📦 Installing Node.js packages..."
npm install --silent

echo "  ✅ Frontend setup complete!"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add the ML model file 'complex_price_model_v2.pkl' to the backend/ directory"
echo "2. Run './start.sh' to start both servers"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "Optional: Run with Docker using 'docker-compose up'"