@echo off
echo 🚀 PUSHING CROP CARE AI TO GITHUB...
echo.

REM Replace YOUR_USERNAME with your actual GitHub username
set /p username="Enter your GitHub username: "

echo Setting remote URL for user: %username%
git remote set-url origin https://github.com/%username%/Crop-Care-AI.git

echo Switching to main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo.
echo ✅ PUSH COMPLETE! Check your GitHub repository at:
echo https://github.com/%username%/Crop-Care-AI
echo.
pause
