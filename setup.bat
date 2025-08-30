@echo off
REM Setup script for Smart Crop Advisory (Windows)

echo 🌾 Setting up Smart Crop Advisory...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate

REM Install backend dependencies
echo 📥 Installing backend dependencies...
pip install -r backend\requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys
)

echo ✅ Setup complete!
echo.
echo 🚀 To start the backend:
echo    uvicorn backend.app:app --reload
echo.
echo 🌐 To start the frontend:
echo    npx serve frontend
echo.
echo 🤖 To start the Telegram bot:
echo    python chatbot\telegram_bot.py

pause
