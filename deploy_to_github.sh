#!/bin/bash
# Quick script to push CleanTrack to GitHub

echo "🚀 CleanTrack - Push to GitHub"
echo "================================"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ GitHub username is required!"
    exit 1
fi

echo ""
echo "📝 Steps to follow:"
echo "1. Go to https://github.com/new"
echo "2. Create a repository named: cleantrack"
echo "3. Do NOT initialize with README"
echo "4. Press Enter when ready..."
read -p ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "🔄 Removing existing origin remote..."
    git remote remove origin
fi

# Add new remote
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/$GITHUB_USER/cleantrack.git

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Code pushed to GitHub!"
    echo ""
    echo "📍 Your repository: https://github.com/$GITHUB_USER/cleantrack"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Go to https://render.com"
    echo "2. Sign up / Log in"
    echo "3. Click 'New +' → 'Blueprint'"
    echo "4. Connect your GitHub repository: $GITHUB_USER/cleantrack"
    echo "5. Follow the instructions in DEPLOY_NOW.md"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "1. Repository doesn't exist on GitHub yet"
    echo "2. Wrong GitHub username"
    echo "3. Need to authenticate with GitHub"
    echo ""
    echo "Try:"
    echo "- Create the repository on GitHub first"
    echo "- Run: git push -u origin main"
fi
