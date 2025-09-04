#!/bin/bash

# GitHub Deployment Script
# Run this after creating your GitHub repository

echo "🚀 Setting up GitHub remote repository..."

# You need to replace YOUR_USERNAME with your actual GitHub username
read -p "Enter your GitHub username: " username

# Add remote repository
git remote add origin https://github.com/$username/crop-care-ai-system.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main

echo "✅ Successfully deployed to GitHub!"
echo "🌐 Your repository: https://github.com/$username/crop-care-ai-system"
echo "🚀 Deploy to Vercel: https://vercel.com/new/clone?repository-url=https://github.com/$username/crop-care-ai-system"
