@echo off
cd /d "%~dp0"

echo ==========================================
echo Gesture-Based AI Controller - Setup
echo ==========================================
echo.

echo Checking Python...
python --version
IF ERRORLEVEL 1 (
    echo Python is not installed.
    echo Please install Python 3.10 and try again.
    pause
    exit
)

echo.
echo Installing required libraries...
pip install -r requirements.txt

echo.
echo Starting Gesture-Based AI Controller...
python ui_app.py

echo.
echo Application closed.
pause
