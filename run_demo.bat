@echo off
REM Batch script to run the complete system demo on Windows

echo ============================================================
echo AI-Powered Faculty Stress Detector - Demo Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if dataset exists
if not exist "dataset.xlsx" (
    echo Dataset not found. Generating dataset...
    python ml_component/generate_dataset.py
    echo.
)

REM Check if model exists, if not train it
if not exist "ml_component\stress_model.pkl" (
    echo Model not found. Training model...
    python ml_component/stress_predictor.py
    echo.
)

REM Run the integrated system
echo Running integrated system...
echo.
python integration/run_system.py

echo.
echo ============================================================
echo Demo completed!
echo ============================================================
echo.
echo Next: Run the Visual Prolog expert system to get recommendations
echo.
pause

