#!/bin/bash

# Hypertension Prediction System - Quick Start Script for Linux/Mac

echo ""
echo "===================================="
echo "Hypertension Prediction System"
echo "Quick Start Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/4] Checking Python installation..."
python3 --version

echo ""
echo "[2/4] Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi

echo ""
echo "[3/4] Verifying installation..."
pip3 show Flask Flask-CORS Flask-JWT-Extended scikit-learn pandas numpy

echo ""
echo "[4/4] Starting application..."
echo ""
echo "===================================="
echo "Application will start at:"
echo "http://localhost:5000"
echo "===================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
