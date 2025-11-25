# Setup Instructions

## Quick Setup Guide

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Dataset (if needed)

If you don't have `dataset.xlsx` or want to regenerate it:

```bash
python ml_component/generate_dataset.py
```

This will create a dataset with 250 faculty records.

### Step 3: Train the ML Model (First Time)

```bash
python ml_component/stress_predictor.py
```

This will:
- Load the dataset
- Calculate WSS for each record
- Train a Random Forest model
- Save the model to `ml_component/stress_model.pkl`

### Step 4: Run the Complete System

```bash
python integration/run_system.py
```

This integrated script will:
1. Load or train the model
2. Prompt for faculty workload input
3. Predict stress level
4. Write output to `integration/stress_output.txt`
5. Provide instructions for running the Prolog system

### Step 5: Run Visual Prolog Expert System

#### Option A: Using Visual Prolog IDE

1. Open Visual Prolog IDE
2. Create a new project or open existing
3. Add `prolog_component/faculty_wellness.pro` to the project
4. Build the project
5. Run the executable

#### Option B: Using Command Line (if Visual Prolog compiler is installed)

```bash
cd prolog_component
vip.exe faculty_wellness.pro
```

The Prolog system will automatically read from `integration/stress_output.txt` and generate recommendations.

## Testing Individual Components

### Test ML Component Only

```bash
python ml_component/predict.py
```

### Test with Sample Data

You can modify `integration/run_system.py` to use hardcoded test data instead of user input for testing.

## Troubleshooting

### Issue: "No module named 'pandas'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: "FileNotFoundError: dataset.xlsx"
**Solution**: Generate the dataset: `python ml_component/generate_dataset.py`

### Issue: Prolog can't read stress_output.txt
**Solution**: 
- Make sure the Python component ran successfully
- Check that `integration/stress_output.txt` exists
- Verify the file format is: `STRESS_LEVEL=High` (or Medium/Low)
- Check file paths (use relative paths or adjust in Prolog code)

### Issue: Model accuracy is low
**Solution**: 
- Ensure dataset has sufficient records (200-300)
- Check data quality in dataset.xlsx
- Retrain the model: `python ml_component/stress_predictor.py`

## File Structure After Setup

```
AuraAI/
├── dataset.xlsx                    # ✓ Should exist
├── ml_component/
│   └── stress_model.pkl           # ✓ Generated after training
├── integration/
│   └── stress_output.txt          # ✓ Generated after prediction
└── ... (other files)
```

## Next Steps

1. Review `PROJECT_DOCUMENTATION.md` for complete system details
2. Test the system with various faculty workload scenarios
3. Customize Prolog rules if needed
4. Prepare demonstration materials

