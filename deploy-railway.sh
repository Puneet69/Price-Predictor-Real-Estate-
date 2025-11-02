#!/bin/bash

# Railway Deployment Script for Property Comparison App
echo "🚀 Preparing Property Comparison App for Railway deployment..."

# Create production environment files
echo "📝 Creating production configuration..."

# Backend production requirements
echo "Creating backend/requirements.txt for production..."
cat > backend/requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pymongo==4.6.0
pandas==2.1.4
matplotlib==3.8.2
seaborn==0.13.0
numpy==1.26.2
python-multipart==0.0.6
python-dotenv==1.0.0
gunicorn==21.2.0
EOF

# Create Procfile for Railway
echo "Creating Procfile..."
cat > Procfile << EOF
web: cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:\$PORT
EOF

# Create railway.json configuration
echo "Creating railway.json..."
cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:\$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create production environment template
echo "Creating .env.production template..."
cat > .env.production.template << EOF
# MongoDB Configuration (Railway will provide this)
MONGODB_URI=\${{MONGODB_PRIVATE_URL}}

# App Configuration
DEBUG=False
ENVIRONMENT=production

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.railway.app,https://your-domain.com

# Optional: Custom domain
CUSTOM_DOMAIN=your-custom-domain.com
EOF

echo "✅ Railway deployment files created!"
echo ""
echo "Next steps:"
echo "1. Push these changes to GitHub"
echo "2. Go to railway.app and connect your GitHub repo"
echo "3. Deploy backend + MongoDB"
echo "4. Deploy frontend separately"
echo ""