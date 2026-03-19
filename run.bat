@echo off
REM Hypertension Prediction System - Quick Start Script for Windows

echo.
echo ====================================
echo Hypertension Prediction System
echo Quick Start Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo.
echo [2/4] Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo [3/4] Verifying installation...
pip show Flask Flask-CORS Flask-JWT-Extended scikit-learn pandas numpy

echo.
echo [4/4] Starting application...
echo.
echo ====================================
echo Application will start at:
echo http://localhost:5000
echo ====================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
