#!/bin/bash

# 🚀 Render Backend + Vercel Frontend Deployment Script
# The optimal deployment strategy for your Property Comparison App

echo "🚀 Render Backend + Vercel Frontend Deployment"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Deployment Strategy:${NC}"
echo "✅ Backend: Render (Python/FastAPI) - FREE"
echo "✅ Frontend: Vercel (React/CDN) - FREE"
echo "✅ Database: MongoDB Atlas - FREE"
echo "✅ Total Cost: $0/month"
echo ""

echo -e "${YELLOW}📋 Prerequisites:${NC}"
echo "✅ GitHub repository: Puneet69/Price-Predictor-Real-Estate-"
echo "✅ MongoDB Atlas configured and tested"
echo "✅ Backend optimized for Render deployment"
echo "✅ Frontend configured for Vercel deployment"
echo ""

echo -e "${GREEN}🔧 Step 1: Deploy Backend to Render${NC}"
echo "1. Go to https://render.com"
echo "2. Sign up with GitHub account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect repository: Puneet69/Price-Predictor-Real-Estate-"
echo "5. Configure:"
echo "   - Name: property-comparison-backend"
echo "   - Root Directory: backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "6. Add Environment Variable:"
echo "   Key: MONGODB_URI"
echo "   Value: mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate"
echo ""
echo "7. Click 'Create Web Service' and wait for deployment"
echo "8. Note your backend URL: https://property-comparison-backend.onrender.com"
echo ""

echo -e "${GREEN}⚡ Step 2: Deploy Frontend to Vercel${NC}"  
echo "1. Go to https://vercel.com"
echo "2. Sign up with GitHub account"
echo "3. Click 'Import Project'"
echo "4. Select repository: Puneet69/Price-Predictor-Real-Estate-"
echo "5. Configure:"
echo "   - Framework Preset: Create React App"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"  
echo "   - Output Directory: build"
echo ""
echo "6. Add Environment Variable:"
echo "   Key: REACT_APP_API_URL"
echo "   Value: https://property-comparison-backend.onrender.com"
echo "   (Use your actual Render backend URL from Step 1)"
echo ""
echo "7. Click 'Deploy' and wait for deployment"
echo "8. Note your frontend URL: https://property-comparison-frontend.vercel.app"
echo ""

echo -e "${BLUE}🌐 Expected Results:${NC}"
echo "Backend API: https://property-comparison-backend.onrender.com"
echo "API Documentation: https://property-comparison-backend.onrender.com/docs"
echo "Frontend App: https://property-comparison-frontend.vercel.app"
echo ""

echo -e "${YELLOW}💰 Cost Breakdown:${NC}"
echo "✅ Render Backend: FREE (750 hours/month)"
echo "✅ Vercel Frontend: FREE (unlimited)"
echo "✅ MongoDB Atlas: FREE (M0 cluster)"
echo "🎉 Total Monthly Cost: \$0"
echo ""

echo -e "${GREEN}🎯 Performance Benefits:${NC}"
echo "✅ Backend: Optimized Python environment"
echo "✅ Frontend: Global CDN with edge caching"
echo "✅ Auto-scaling: Both platforms handle traffic spikes"
echo "✅ Auto-deploy: Push to GitHub → automatic redeployment"
echo ""

echo -e "${BLUE}🛠️ Quick Troubleshooting:${NC}"
echo "• Backend sleeping? First request wakes it (10-30 seconds)"
echo "• CORS errors? Check REACT_APP_API_URL is correct"
echo "• Build fails? Verify environment variables are set"
echo ""

echo -e "${GREEN}🚀 One-Click Deploy Links:${NC}"
echo "Render Backend: https://render.com/deploy?repo=https://github.com/Puneet69/Price-Predictor-Real-Estate-"
echo "Vercel Frontend: https://vercel.com/new/clone?repository-url=https://github.com/Puneet69/Price-Predictor-Real-Estate-&root-directory=frontend"
echo ""

echo -e "${YELLOW}📚 Documentation:${NC}"
echo "Complete Guide: RENDER_VERCEL_DEPLOYMENT.md"
echo "Render Config: render.yaml"
echo "Vercel Config: vercel.json"
echo ""

# Optional: Open deployment pages
read -p "Would you like to open Render and Vercel in your browser? (y/n): " -n 1 -r
echo
if [[ \$REPLY =~ ^[Yy]\$ ]]; then
    echo "Opening Render..."
    open https://render.com
    sleep 2
    echo "Opening Vercel..."
    open https://vercel.com
fi

echo ""
echo -e "${GREEN}🎉 Ready for Hybrid Deployment!${NC}"
echo "Deploy backend to Render first, then frontend to Vercel!"
echo "Total deployment time: ~10 minutes"
echo ""