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
