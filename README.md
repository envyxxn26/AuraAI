# AuraAI - AI-Powered Faculty Stress Detector and Wellness Recommendation Expert System

A hybrid intelligent system that combines machine learning (Python) and rule-based expert systems (Visual Prolog) to predict faculty stress levels and provide personalized wellness recommendations.

## 🎯 Project Overview

This system consists of two integrated components:

1. **Machine Learning Component (Python)**: Predicts faculty stress levels (Low, Medium, High) based on workload factors using Workload Stress Score (WSS) calculation and Random Forest classification.

2. **Rule-Based Expert System (Visual Prolog)**: Generates personalized wellness and workload recommendations using a knowledge base and expert rules.

## 📋 Features

- **Stress Level Prediction**: Calculates Workload Stress Score (WSS) from 9 workload factors
- **ML Model Training**: Random Forest classifier for accurate predictions
- **Expert Recommendations**: Rule-based system providing actionable wellness advice
- **Seamless Integration**: File-based communication between Python and Prolog components
- **Comprehensive Documentation**: Complete project documentation and usage instructions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Visual Prolog 7.x or later
- Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AuraAI
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Option 1: Run Complete System (Recommended)

```bash
python integration/run_system.py
```

This will:
1. Load or train the ML model
2. Prompt for faculty workload input
3. Predict stress level
4. Generate output file for Prolog system
5. Provide instructions for running the expert system

#### Option 2: Run Components Separately

**Step 1: Train ML Model (First Time Only)**
```bash
python ml_component/stress_predictor.py
```

**Step 2: Make Predictions**
```bash
python ml_component/predict.py
```

**Step 3: Run Prolog Expert System**
- Open Visual Prolog IDE
- Load `prolog_component/faculty_wellness.pro`
- Build and run the project

## 📁 Project Structure

```
AuraAI/
├── dataset.xlsx                    # Training dataset (200-300 records)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── PROJECT_DOCUMENTATION.md        # Complete project documentation
├── ml_component/
│   ├── stress_predictor.py        # Main ML module with WSS calculation
│   ├── predict.py                 # Standalone prediction interface
│   └── stress_model.pkl           # Trained model (auto-generated)
├── prolog_component/
│   └── faculty_wellness.pro       # Visual Prolog expert system
└── integration/
    ├── stress_output.txt          # Communication file (auto-generated)
    └── run_system.py              # Integration script
```

## 🔬 How It Works

### Workload Stress Score (WSS) Calculation

The system calculates a WSS (9-27 points) based on 9 factors:

| Factor | Low (1pt) | Medium (2pts) | High (3pts) |
|--------|-----------|---------------|-------------|
| Subjects | 1-2 | 3-4 | 5+ |
| Students | <60 | 60-100 | >100 |
| Prep Hours | <6 | 6-10 | >10 |
| Research | <4 | 4-6 | >6 |
| Committees | 0-1 | 2 | 3+ |
| Admin Tasks | 0-1 | 2-3 | 4+ |
| Meetings | <3 | 3-6 | >6 |
| Sleep | 7+ | 6 | <6 |
| Weekend Work | 0 | 1-2 | 3+ |

**Stress Level Categories:**
- **Low Stress**: WSS 9-14
- **Medium Stress**: WSS 15-20
- **High Stress**: WSS 21-27

### Expert System Rules

The Prolog system contains:
- **12+ Knowledge Base Facts**: About faculty wellness and workload patterns
- **6+ Expert Rules**: Mapping stress levels to specific recommendations

## 📊 Example Output

### ML Component Output:
```
Workload Stress Score (WSS): 19/27
Predicted Stress Level: Medium Stress
```

### Expert System Output:
```
STRESS LEVEL: MEDIUM
-------------------

PREVENTIVE MEASURES RECOMMENDED:

1. TIME-BLOCKING STRATEGIES:
   - Allocate specific time blocks for teaching prep (2-3 hours/day)
   - Reserve morning hours for research
   ...

REASONING EXPLANATION:
Rule Applied: MEDIUM_STRESS_RULE
Conditions Met:
  - Workload Stress Score (WSS) is 15-20
  - Moderate workload intensity
  ...
```

## 📖 Documentation

For complete documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

The documentation includes:
- Detailed methodology
- Dataset description
- ML approach explanation
- Prolog knowledge base structure
- Integration workflow
- System outputs
- Reflection and insights

## 🛠️ Development

### Adding New Rules

To add new rules to the Prolog expert system, edit `prolog_component/faculty_wellness.pro` and add new rule predicates following the existing pattern.

### Modifying WSS Calculation

Edit the `calculate_wss()` method in `ml_component/stress_predictor.py` to adjust point allocations or add new factors.

## 📝 Requirements

This project was developed for:
- **Course**: CS18a - Artificial Intelligence and Machine Learning
- **Project Type**: Hybrid AI System (Python + Visual Prolog)
- **Group Size**: 2 Members

## 🤝 Contributing

This is an academic project. For improvements or suggestions, please create an issue or pull request.

## 📄 License

This project is for academic purposes.

## 👥 Authors

- Member 1: ML Component Development
- Member 2: Expert System Development

---

**Note**: Make sure to have the `dataset.xlsx` file in the root directory for training the model. The dataset should contain faculty workload data with the specified columns.
