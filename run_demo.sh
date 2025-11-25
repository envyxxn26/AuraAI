#!/bin/bash
# Shell script to run the complete system demo on Linux/Mac

echo "============================================================"
echo "AI-Powered Faculty Stress Detector - Demo Script"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if dataset exists
if [ ! -f "dataset.xlsx" ]; then
    echo "Dataset not found. Generating dataset..."
    python3 ml_component/generate_dataset.py
    echo ""
fi

# Check if model exists, if not train it
if [ ! -f "ml_component/stress_model.pkl" ]; then
    echo "Model not found. Training model..."
    python3 ml_component/stress_predictor.py
    echo ""
fi

# Run the integrated system
echo "Running integrated system..."
echo ""
python3 integration/run_system.py

echo ""
echo "============================================================"
echo "Demo completed!"
echo "============================================================"
echo ""
echo "Next: Run the Visual Prolog expert system to get recommendations"
echo ""

