#!/bin/bash
# Setup script for Smart Crop Advisory

echo "🌾 Setting up Smart Crop Advisory..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install backend dependencies
echo "📥 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys"
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the backend:"
echo "   uvicorn backend.app:app --reload"
echo ""
echo "🌐 To start the frontend:"
echo "   npx serve frontend"
echo ""
echo "🤖 To start the Telegram bot:"
echo "   python chatbot/telegram_bot.py"
