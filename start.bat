@echo off
echo Starting Smart Crop Advisory System...
echo.

echo 🚀 Starting Backend Server...
start "Backend Server" cmd /k "cd /d \"%~dp0backend\" && C:/Users/asus/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m uvicorn app:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d \"%~dp0frontend\" && C:/Users/asus/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m http.server 3000"

timeout /t 2 /nobreak >nul

echo.
echo ✅ System started successfully!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo Press any key to open the frontend in your browser...
pause >nul
start http://localhost:3000
