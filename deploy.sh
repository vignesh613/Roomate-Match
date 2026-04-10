#!/bin/bash

echo "🚀 Roommate Match - Deployment Script"
echo "===================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Navigate to backend directory
cd backend

# Initialize Railway project
echo "🚂 Initializing Railway project..."
railway init --name "roommate-match"

# Deploy
echo "📤 Deploying to Railway..."
railway up

# Prompt for API key
echo ""
echo "🔑 Please set your OpenAI API key:"
echo "railway variables set OPENAI_API_KEY=your_openai_api_key_here"
echo ""
echo "📋 Get your API key from: https://platform.openai.com/api-keys"
echo ""
echo "🌐 Your app will be available at the URL shown above once deployment completes!"