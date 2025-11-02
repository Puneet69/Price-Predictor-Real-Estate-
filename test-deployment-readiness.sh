#!/bin/bash

# 🧪 Deployment Test Script
echo "🧪 Testing Property Comparison App deployment readiness..."

# Check if required files exist
echo "📋 Checking deployment files..."

required_files=(
    "Procfile"
    "railway.json"
    "backend/requirements.txt"
    "backend/Dockerfile"
    "frontend/Dockerfile"
    "docker-compose.yml"
    ".do/app.yaml"
    "DEPLOYMENT_GUIDE.md"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        missing_files+=("$file")
    fi
done

# Check Docker setup
echo ""
echo "🐳 Testing Docker setup..."
if command -v docker &> /dev/null && docker --version &> /dev/null; then
    echo "   ✅ Docker is installed"
    
    # Test docker-compose
    if command -v docker-compose &> /dev/null; then
        echo "   ✅ Docker Compose is available"
        echo "   📋 You can run: docker-compose up -d"
    else
        echo "   ⚠️  Docker Compose not found (optional)"
    fi
else
    echo "   ⚠️  Docker not installed (needed for local deployment)"
fi

# Check Python dependencies
echo ""
echo "🐍 Checking Python environment..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "   ✅ $python_version"
    
    # Check if in virtual environment
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "   ✅ Virtual environment active: $VIRTUAL_ENV"
    else
        echo "   ⚠️  Virtual environment not active (recommended for local dev)"
    fi
else
    echo "   ❌ Python3 not found"
fi

# Check Node.js
echo ""
echo "📦 Checking Node.js environment..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "   ✅ Node.js $node_version"
    
    if command -v npm &> /dev/null; then
        npm_version=$(npm --version)
        echo "   ✅ npm $npm_version"
    else
        echo "   ❌ npm not found"
    fi
else
    echo "   ❌ Node.js not found"
fi

# Check MongoDB
echo ""
echo "🍃 Checking MongoDB..."
if command -v mongod &> /dev/null; then
    echo "   ✅ MongoDB installed locally"
elif command -v mongo &> /dev/null; then
    echo "   ✅ MongoDB client available"
else
    echo "   ⚠️  MongoDB not installed locally (use cloud database for deployment)"
fi

# Summary
echo ""
echo "📊 Deployment Readiness Summary:"
if [ ${#missing_files[@]} -eq 0 ]; then
    echo "   ✅ All deployment files present"
    echo "   🚀 Ready for deployment!"
else
    echo "   ❌ Missing files: ${missing_files[*]}"
    echo "   📝 Create missing files before deployment"
fi

echo ""
echo "🎯 Next Steps:"
echo "   1. Choose deployment platform (Railway, Render, DigitalOcean)"
echo "   2. Follow DEPLOYMENT_GUIDE.md instructions"
echo "   3. Push changes to GitHub"
echo "   4. Connect repository to chosen platform"
echo ""
echo "📚 Available deployment options:"
echo "   • Railway: https://railway.app (easiest)"
echo "   • Render: https://render.com (free tier)"
echo "   • DigitalOcean: https://digitalocean.com (production)"
echo "   • Local Docker: docker-compose up -d"
echo ""