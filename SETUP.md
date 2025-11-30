# Setup Instructions - Running on Another Computer

## Quick Start

### 1. Copy the Project
Copy the entire `AuraAI` folder to the new computer.

### 2. Install Python Dependencies
```bash
cd AuraAI
pip install -r requirements.txt
```

### 3. Run the System
```bash
python integration/run_system.py
```

That's it! The system will:
- Automatically train the model if needed (first run)
- Work with the pre-built Prolog executable (Windows)
- Handle everything automatically

---

## Detailed Setup

### Requirements
- **Python 3.8+** installed
- **Windows** (for Prolog executable) OR **Visual Prolog** (to build from source)

### Step-by-Step

#### Step 1: Copy Files
Copy these folders/files to the new computer:
```
AuraAI/
├── dataset.xlsx                    # REQUIRED
├── requirements.txt                # REQUIRED
├── ml_component/                   # REQUIRED
│   ├── stress_predictor.py
│   ├── predict.py
│   └── generate_dataset.py
├── integration/                    # REQUIRED
│   └── run_system.py
└── prolog_component/               # OPTIONAL (for full functionality)
    └── faculty_wellness/
        └── exe64/                  # Windows executable + DLLs
            ├── faculty_wellness.exe
            ├── vipKernel.dll
            └── vipRun.dll
```

#### Step 2: Install Python Packages
Open terminal/command prompt in the AuraAI folder:
```bash
pip install -r requirements.txt
```

This installs:
- pandas
- numpy
- scikit-learn
- openpyxl

#### Step 3: Run the System
```bash
python integration/run_system.py
```

The first run will:
- Train the ML model (takes a few seconds)
- Save the model to `ml_component/stress_model.pkl`
- Be ready to use

---

## Recompiling Prolog Component (If Needed)

### Option A: Use Pre-built Executable (Easiest)
- Copy the `prolog_component/faculty_wellness/exe64/` folder
- **No Visual Prolog needed** - just copy and run
- Works on Windows only

### Option B: Build from Source
If you need to modify or rebuild the Prolog code:

1. **Install Visual Prolog 7.x or later**
   - Download from: https://www.visual-prolog.com/

2. **Open the Project**
   - Open Visual Prolog IDE
   - File → Open → Project
   - Navigate to `prolog_component/faculty_wellness/faculty_wellness.vipprj`
   - Click Open

3. **Build the Project**
   - Press `Ctrl+Shift+B` (or Build → Build)
   - Wait for "Build succeeded"

4. **Find the Executable**
   - The executable will be in: `prolog_component/faculty_wellness/exe64/faculty_wellness.exe`
   - DLLs (`vipKernel.dll`, `vipRun.dll`) will be in the same folder

---

## Troubleshooting

### "ModuleNotFoundError"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "Dataset not found"
**Solution**: Make sure `dataset.xlsx` is in the root AuraAI folder

### "Prolog executable not found"
**Solution**: 
- Copy `prolog_component/faculty_wellness/exe64/` folder, OR
- Build from source using Visual Prolog (see Option B above)

### Model Accuracy Issues
**Solution**: Delete `ml_component/stress_model.pkl` and let it retrain

---

## File Structure After Setup

```
AuraAI/
├── dataset.xlsx                    # Training data
├── requirements.txt                # Python dependencies
├── ml_component/
│   ├── stress_predictor.py        # ML code
│   └── stress_model.pkl           # Trained model (auto-generated)
├── integration/
│   └── run_system.py              # Main script
└── prolog_component/
    └── faculty_wellness/
        └── exe64/
            ├── faculty_wellness.exe  # Prolog executable
            ├── vipKernel.dll
            └── vipRun.dll
```

---

## Quick Test

After setup, test the system:
```bash
python integration/run_system.py
```

Then:
1. Select option 1 (Enter new faculty data)
2. Press Enter for all prompts (uses defaults)
3. Should show prediction results
4. Optionally run Prolog expert system

---

## Notes

- **Visual Prolog is NOT required** to run - only to build/compile
- The executable in `exe64/` is standalone and works without Visual Prolog
- Python component works on Windows, Linux, and Mac
- Prolog executable is Windows-only (unless built from source on other OS)

