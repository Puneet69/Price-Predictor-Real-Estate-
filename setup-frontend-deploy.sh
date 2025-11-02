# Frontend Deployment Configuration

# Create production build script
echo "📦 Creating frontend production build..."

# Update frontend package.json with build optimization
cd frontend

# Install serve for production serving
npm install --save-dev serve

# Create production environment file
cat > .env.production << EOF
REACT_APP_API_URL=https://your-backend-url.railway.app
GENERATE_SOURCEMAP=false
EOF

# Create production build script
cat > build-production.sh << EOF
#!/bin/bash
echo "🏗️ Building Property Comparison App frontend for production..."

# Install dependencies
npm ci --only=production

# Build the app
npm run build

# Test the build locally (optional)
echo "📋 To test production build locally, run:"
echo "npx serve -s build -l 3000"

echo "✅ Production build complete!"
echo "📁 Built files are in the 'build' directory"
EOF

chmod +x build-production.sh

echo "✅ Frontend deployment configuration created!"
echo "📁 Files created:"
echo "   - .env.production (API URL configuration)"
echo "   - build-production.sh (production build script)"