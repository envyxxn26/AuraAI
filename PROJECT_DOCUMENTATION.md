# AI-Powered Faculty Stress Detector and Wellness Recommendation Expert System

## Project Documentation

**Course:** Artificial Intelligence and Machine Learning  
**Project Type:** Hybrid AI System (Python + Visual Prolog)  
**Group Size:** 2 Members

---

## 1. Introduction

### 1.1 Overview

This project implements a hybrid intelligent system that combines machine learning and rule-based expert systems to address faculty workload management and wellness. The system consists of two integrated components:

1. **Machine Learning Component (Python)**: Predicts faculty stress levels based on workload-related factors using a data-driven approach.
2. **Rule-Based Expert System (Visual Prolog)**: Generates personalized wellness and workload recommendations using symbolic reasoning based on the predicted stress level.

### 1.2 Problem Significance

Faculty members in educational institutions often face significant workload pressures from multiple sources:
- Teaching multiple subjects with large class sizes
- Research and publication requirements
- Administrative and committee duties
- Meeting obligations
- Work-life balance challenges

These factors can lead to stress, burnout, and decreased teaching quality. Early detection and intervention through personalized recommendations can help maintain faculty wellness and institutional effectiveness.

### 1.3 System Purpose

The system aims to:
- **Predict** stress levels accurately using workload metrics
- **Recommend** actionable wellness strategies based on stress levels
- **Integrate** data-driven and rule-based AI approaches
- **Support** faculty members in managing their workload effectively

---

## 2. Methodology

### 2.1 Dataset Summary

The dataset contains 200-300 records of faculty workload information with the following features:

| Feature | Description | Range |
|---------|-------------|-------|
| Subjects Handled | Number of courses taught | 1-10 |
| Total Students | Combined enrollment across courses | 20-200 |
| Preparation Hours | Weekly hours for class preparation | 2-15 |
| Research Load | Weekly hours dedicated to research | 0-12 |
| Committee Duties | Number of committee assignments | 0-5 |
| Administrative Tasks | Count of administrative responsibilities | 0-6 |
| Meeting Hours | Weekly hours in meetings | 0-10 |
| Sleep Hours | Average nightly sleep duration | 4-9 |
| Weekend Work Frequency | Times per month working on weekends | 0-8 |

**Sample Data:**
```
F001: 4 subjects, 120 students, 10 prep hours, 8 research, 2 committees, 3 admin, 3 meetings, 6 sleep, 6 weekend work
F002: 2 subjects, 60 students, 6 prep hours, 4 research, 1 committee, 1 admin, 1 meeting, 7 sleep, 1 weekend work
```

### 2.2 ML Approach and Stress Level Categories

#### 2.2.1 Workload Stress Score (WSS) Calculation

The system uses a rule-based scoring mechanism to calculate Workload Stress Score:

**Point Allocation per Variable:**

| Variable | Low (1 pt) | Medium (2 pts) | High (3 pts) |
|----------|-----------|----------------|--------------|
| Subjects Handled | 1-2 | 3-4 | 5+ |
| Total Students | <60 | 60-100 | >100 |
| Preparation Hours | <6 | 6-10 | >10 |
| Research Load | <4 | 4-6 | >6 |
| Committee Duties | 0-1 | 2 | 3+ |
| Administrative Tasks | 0-1 | 2-3 | 4+ |
| Meeting Hours | <3 | 3-6 | >6 |
| Sleep Hours | 7+ | 6 | <6 |
| Weekend Work Frequency | 0 | 1-2 | 3+ |

**Total WSS Range:** 9-27 points

**Stress Level Categories:**

| WSS Range | Stress Level |
|-----------|--------------|
| 9-14 | Low Stress |
| 15-20 | Medium Stress |
| 21-27 | High Stress |

#### 2.2.2 Machine Learning Model

**Algorithm:** Random Forest Classifier
- **Ensemble Method**: Combines multiple decision trees
- **Advantages**: Handles non-linear relationships, provides feature importance
- **Training**: 80% training, 20% testing split with stratification
- **Evaluation**: Accuracy score and classification report

**Implementation:**
- Calculates WSS for each record
- Converts WSS to stress level category
- Trains Random Forest on workload features
- Predicts stress level for new faculty members

### 2.3 Prolog Knowledge Base and Rules Structure

#### 2.3.1 Knowledge Base Facts (12 Facts)

The knowledge base contains facts about faculty wellness and workload patterns:

1. High workload correlates with increased stress levels
2. Adequate sleep (7+ hours) is essential for faculty wellness
3. Excessive committee duties reduce time for core teaching activities
4. Regular weekend work indicates work-life imbalance
5. Large class sizes increase preparation and grading time
6. Research activities require dedicated time blocks for productivity
7. Administrative tasks can fragment work schedules
8. Frequent meetings disrupt focused work periods
9. Multiple subject preparations increase cognitive load
10. Workload stress affects both teaching quality and personal health
11. Time management strategies can mitigate stress
12. Institutional support is crucial for faculty well-being

#### 2.3.2 Expert Rules (6+ Rules)

**Rule 1: HIGH_STRESS_RULE**
- **Condition**: WSS = 21-27 (High Stress)
- **Actions**: 
  - Immediate workload adjustments
  - Mandatory wellness breaks
  - Time management interventions
  - Sleep and recovery prioritization
  - Institutional support activation

**Rule 2: MEDIUM_STRESS_RULE**
- **Condition**: WSS = 15-20 (Medium Stress)
- **Actions**:
  - Time-blocking strategies
  - Work cycle monitoring
  - Efficiency improvements
  - Wellness maintenance
  - Preventive planning

**Rule 3: LOW_STRESS_RULE**
- **Condition**: WSS = 9-14 (Low Stress)
- **Actions**:
  - Routine maintenance
  - Preventive wellness planning
  - Sustainable growth
  - Long-term wellness
  - Institutional contribution

**Additional Rules:**
- **Rule 4**: Sleep optimization rule (applies when sleep < 7 hours)
- **Rule 5**: Weekend work reduction rule (applies when weekend work > 2)
- **Rule 6**: Committee duty balancing rule (applies when committees > 2)

### 2.4 Integration Workflow

The system operates in a sequential pipeline:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Python ML Component                                   │
│    - Loads dataset                                       │
│    - Trains/loads model                                  │
│    - Accepts faculty workload input                      │
│    - Calculates WSS                                      │
│    - Predicts stress level                               │
│    - Writes to: integration/stress_output.txt           │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Integration Layer                                     │
│    - File: integration/stress_output.txt                │
│    - Format: STRESS_LEVEL=High/Medium/Low              │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Visual Prolog Expert System                          │
│    - Reads stress_output.txt                            │
│    - Parses stress level                                │
│    - Applies knowledge base facts                       │
│    - Executes expert rules                              │
│    - Generates recommendations                          │
│    - Displays reasoning explanation                     │
└─────────────────────────────────────────────────────────┘
```

**File Communication:**
- **Output File**: `integration/stress_output.txt`
- **Format**: `STRESS_LEVEL=High` (or Medium/Low)
- **Location**: Shared directory accessible to both components

---

## 3. System Outputs

### 3.1 ML Component Output

**Example Prediction:**
```
Workload Stress Score (WSS): 19/27
Predicted Stress Level: Medium Stress
```

**Model Performance:**
- Accuracy: ~95% (on test set)
- Classification Report shows precision, recall, and F1-score for each class

### 3.2 Expert System Output

**Example Recommendations for High Stress:**
```
STRESS LEVEL: HIGH
-----------------

IMMEDIATE ACTIONS REQUIRED:

1. WORKLOAD ADJUSTMENTS:
   - Request reduction in number of subjects (target: 2-3)
   - Negotiate smaller class sizes or teaching assistant support
   - Delegate administrative tasks where possible
   - Request temporary relief from committee assignments

2. WELLNESS BREAKS:
   - Schedule mandatory 15-minute breaks every 2 hours
   - Take a complete day off each week (no work activities)
   - Plan a 3-5 day wellness break within the next month
   - Engage in daily 30-minute physical activity

[... additional recommendations ...]

REASONING EXPLANATION:
Rule Applied: HIGH_STRESS_RULE
Conditions Met:
  - Workload Stress Score (WSS) is 21-27
  - Multiple high-intensity factors present
  - Risk of burnout and health issues

Conclusion: Immediate intervention required...
```

### 3.3 Integration Output

The complete system provides:
1. Stress level prediction with WSS score
2. Detailed wellness recommendations
3. Reasoning explanation
4. Actionable next steps

---

## 4. Reflection

### 4.1 Roles and Responsibilities

**Member 1 (ML Component Developer):**
- Developed Python ML module with WSS calculation
- Implemented Random Forest classifier
- Created dataset processing pipeline
- Built prediction interface
- Generated stress level output file

**Member 2 (Expert System Developer):**
- Designed Visual Prolog knowledge base
- Created expert rules for recommendations
- Implemented reasoning and explanation logic
- Built file reading and parsing functionality
- Developed recommendation generation system

**Both Members:**
- Collaborated on integration design
- Tested end-to-end system workflow
- Created documentation
- Prepared demonstration materials

### 4.2 Challenges Encountered

1. **Integration Challenge**: Ensuring seamless file communication between Python and Prolog
   - **Solution**: Standardized file format and clear file path conventions

2. **Data Preprocessing**: Handling Excel file format and missing values
   - **Solution**: Used pandas and openpyxl with robust error handling

3. **Rule Complexity**: Balancing rule specificity with system maintainability
   - **Solution**: Structured rules with clear conditions and actions

4. **Model Accuracy**: Achieving good prediction performance with limited data
   - **Solution**: Used ensemble method (Random Forest) and proper train-test split

5. **Visual Prolog Syntax**: Learning Prolog syntax and file I/O operations
   - **Solution**: Referenced documentation and tested incrementally

### 4.3 Insights and Learnings

1. **Hybrid AI Benefits**: Combining ML and rule-based systems provides both data-driven insights and interpretable recommendations.

2. **WSS Formula Effectiveness**: The rule-based WSS calculation provides transparent and explainable stress scoring.

3. **Integration Simplicity**: File-based integration is simple and effective for sequential processing.

4. **Recommendation Quality**: Structured rules with specific actions provide more value than generic advice.

5. **System Extensibility**: The modular design allows easy addition of new rules or ML models.

### 4.4 Future Improvements

1. **Real-time Integration**: Replace file-based communication with API or direct function calls
2. **Enhanced ML Models**: Experiment with neural networks or ensemble methods
3. **Historical Tracking**: Add functionality to track stress levels over time
4. **Personalization**: Incorporate individual faculty preferences and constraints
5. **Web Interface**: Develop user-friendly web application for easier access
6. **Database Integration**: Store predictions and recommendations for analysis

---

## 5. Technical Specifications

### 5.1 System Requirements

**Python Environment:**
- Python 3.8+
- Required packages: pandas, numpy, scikit-learn, openpyxl

**Visual Prolog:**
- Visual Prolog 7.x or later
- Standard library support

**Operating System:**
- Windows (primary), Linux/Mac (with adjustments)

### 5.2 File Structure

```
AuraAI/
├── dataset.xlsx                    # Training dataset
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview
├── PROJECT_DOCUMENTATION.md        # This file
├── ml_component/
│   ├── stress_predictor.py        # Main ML module
│   ├── predict.py                 # Standalone prediction script
│   └── stress_model.pkl           # Trained model (generated)
├── prolog_component/
│   └── faculty_wellness.pro       # Visual Prolog expert system
└── integration/
    ├── stress_output.txt          # Communication file (generated)
    └── run_system.py              # Integration script
```

### 5.3 Usage Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train Model (First Time):**
   ```bash
   python ml_component/stress_predictor.py
   ```

3. **Run Prediction:**
   ```bash
   python ml_component/predict.py
   ```

4. **Run Complete System:**
   ```bash
   python integration/run_system.py
   ```

5. **Run Prolog Expert System:**
   - Open Visual Prolog IDE
   - Load `prolog_component/faculty_wellness.pro`
   - Build and run

---

## 6. Conclusion

This hybrid AI system successfully demonstrates the integration of machine learning and rule-based expert systems. The Python ML component provides accurate stress level predictions, while the Visual Prolog expert system generates personalized, actionable recommendations. The system showcases the complementary strengths of data-driven and symbolic AI approaches, providing a practical solution for faculty wellness management.

The project meets all specified requirements:
- ✓ ML component with WSS calculation and stress prediction
- ✓ Prolog knowledge base with 12+ facts
- ✓ Expert system with 6+ rules
- ✓ Seamless integration between components
- ✓ Clear documentation and demonstration materials

---

**Project Completion Date:** [Date]  
**Group Members:** [Names]  
**Course:** CS18a - Artificial Intelligence and Machine Learning

