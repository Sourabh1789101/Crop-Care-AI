@echo off
REM Setup script for Smart Crop Advisory (Windows)

echo 🌾 Setting up Smart Crop Advisory...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install backend dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the backend:
echo    cd services ^&^& python run_server.py
echo    OR
echo    uvicorn api.index:app --reload
echo.
echo 🌐 To start the frontend:
echo    npx serve frontend
echo.
echo 📖 API Documentation:
echo    http://localhost:8000/docs

pause
