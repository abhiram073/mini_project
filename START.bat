@echo off
echo ========================================
echo Traffic Violation Detection App
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Starting from: %CD%
echo.

echo IMPORTANT: The first time you run this, it will download the AI model.
echo This may take a few minutes. Please be patient.
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Starting the web application...
echo.
echo ========================================
echo SUCCESS! Your website is now running!
echo ========================================
echo.
echo Open your web browser and go to:
echo http://localhost:8000
echo.
echo To stop the application, press Ctrl+C
echo ========================================
echo.

python start_website.py

echo.
echo Application stopped.
pause
