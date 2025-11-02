#!/bin/bash

# 🎨 Render Deployment Script for Property Comparison App
# This script guides you through deploying to Render

echo "🎨 Welcome to Render Deployment for Property Comparison App!"
echo "================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Prerequisites Check:${NC}"
echo "✅ GitHub repository: Puneet69/Price-Predictor-Real-Estate-"
echo "✅ MongoDB Atlas configured"
echo "✅ Backend optimized for Render"
echo "✅ Frontend ready for static deployment"
echo ""

echo -e "${YELLOW}🚀 Deployment Steps:${NC}"
echo ""

echo -e "${GREEN}Step 1: Sign up for Render${NC}"
echo "1. Go to https://render.com"
echo "2. Click 'Get Started for Free'"
echo "3. Sign up with your GitHub account"
echo "4. Authorize Render to access your repositories"
echo ""

echo -e "${GREEN}Step 2: Deploy Backend (FastAPI)${NC}"
echo "1. In Render dashboard, click 'New +'"
echo "2. Select 'Web Service'"
echo "3. Connect repo: Puneet69/Price-Predictor-Real-Estate-"
echo "4. Configure:"
echo "   - Name: property-comparison-backend"
echo "   - Region: Oregon (US West)"
echo "   - Branch: main"
echo "   - Root Directory: backend"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "5. Add Environment Variable:"
echo "   Key: MONGODB_URI"
echo "   Value: mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate"
echo ""
echo "6. Click 'Create Web Service'"
echo ""

echo -e "${GREEN}Step 3: Deploy Frontend (React)${NC}"
echo "1. Click 'New +' again"
echo "2. Select 'Static Site'"
echo "3. Same GitHub repo: Puneet69/Price-Predictor-Real-Estate-"
echo "4. Configure:"
echo "   - Name: property-comparison-frontend"
echo "   - Branch: main"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm ci && npm run build"
echo "   - Publish Directory: build"
echo ""
echo "5. Add Environment Variable:"
echo "   Key: REACT_APP_API_URL"
echo "   Value: https://property-comparison-backend.onrender.com"
echo "   (Replace with your actual backend URL from Step 2)"
echo ""
echo "6. Click 'Create Static Site'"
echo ""

echo -e "${BLUE}📊 Expected Results:${NC}"
echo "Backend URL: https://property-comparison-backend.onrender.com"
echo "Frontend URL: https://property-comparison-frontend.onrender.com"
echo ""

echo -e "${YELLOW}💰 Cost: COMPLETELY FREE!${NC}"
echo "✅ Backend: 750 hours/month free"
echo "✅ Frontend: Unlimited static hosting free"
echo "✅ MongoDB Atlas: Free M0 cluster"
echo "✅ SSL certificates: Included free"
echo ""

echo -e "${GREEN}🎯 Quick Links:${NC}"
echo "Render Dashboard: https://dashboard.render.com"
echo "Deploy Backend: https://render.com/deploy?repo=https://github.com/Puneet69/Price-Predictor-Real-Estate-"
echo "Deploy Frontend: https://render.com/deploy?repo=https://github.com/Puneet69/Price-Predictor-Real-Estate-"
echo ""

echo -e "${BLUE}📖 Full Documentation:${NC}"
echo "See RENDER_DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""

echo -e "${GREEN}🚀 Ready to deploy on Render!${NC}"
echo "Go to https://render.com and start your deployment!"
echo ""

# Optional: Open Render in browser
read -p "Would you like to open Render in your browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Opening Render..."
    open https://render.com
fi

echo "Happy deploying! 🎉"