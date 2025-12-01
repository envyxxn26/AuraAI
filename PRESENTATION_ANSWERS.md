# AI-Powered Faculty Stress Detector - Presentation Answers

## 1. How the Stress Level is Predicted

### Overview
The stress level prediction uses a **hybrid approach** combining:
- **Workload Stress Score (WSS) calculation** (rule-based)
- **Random Forest Machine Learning model** (data-driven)

### Step-by-Step Process

#### Step 1: Data Collection
The system collects 9 workload factors from faculty:
1. **Subjects Handled** (1-10)
2. **Total Students** (20-300)
3. **Preparation Hours** per week (1-20)
4. **Research Load Hours** per week (0-15)
5. **Committee Duties** count (0-5)
6. **Administrative Tasks** count (0-5)
7. **Meeting Hours** per week (0-15)
8. **Sleep Hours** per night (4-10)
9. **Weekend Work Frequency** (times per month, 0-4)

#### Step 2: Workload Stress Score (WSS) Calculation
Each factor is scored from 1-3 points based on intensity:

| Factor | Low (1 pt) | Medium (2 pts) | High (3 pts) |
|--------|------------|-----------------|--------------|
| Subjects | 1-2 | 3-4 | 5+ |
| Students | <60 | 60-100 | >100 |
| Prep Hours | <6 | 6-10 | >10 |
| Research | <4 | 4-6 | >6 |
| Committees | 0-1 | 2 | 3+ |
| Admin Tasks | 0-1 | 2-3 | 4+ |
| Meetings | <3 | 3-6 | >6 |
| Sleep | 7+ hours | 6 hours | <6 hours |
| Weekend Work | 0 | 1-2 | 3+ |

**Total WSS Range: 9-27 points**

#### Step 3: Stress Level Classification
The WSS is converted to stress level:
- **Low Stress**: WSS ≤ 14
- **Medium Stress**: WSS 15-20
- **High Stress**: WSS 21-27

#### Step 4: Machine Learning Model (Supporting)
A **Random Forest Classifier** is also trained on historical data:
- **Algorithm**: Random Forest (200 trees)
- **Training Data**: 500 faculty records from `dataset.xlsx`
- **Features**: Same 9 workload factors
- **Target**: Stress levels (Low/Medium/High)
- **Accuracy**: ~100% (on balanced dataset)

The model provides a secondary prediction, but **WSS-based prediction is used as the primary result** for consistency and interpretability.

#### Step 5: Output Generation
The prediction is written to `integration/stress_output.txt` in the format:
```
STRESS_LEVEL=High
```
(or `Medium` or `Low`)

---

## 2. How the Expert System Provides Recommendations

### Overview
The Visual Prolog expert system uses **rule-based reasoning** to generate personalized wellness recommendations based on the predicted stress level.

### Architecture

#### Knowledge Base
The system maintains 12 expert facts about faculty workload and wellness:
1. High workload correlates with increased stress levels
2. Adequate sleep (7+ hours) is essential for faculty wellness
3. Excessive committee duties reduce time for core teaching activities
4. Regular weekend work indicates work-life imbalance
5. Large class sizes increase preparation and grading time
6. Research activities require dedicated time blocks
7. Administrative tasks can fragment work schedules
8. Frequent meetings disrupt focused work periods
9. Multiple subject preparations increase cognitive load
10. Workload stress affects teaching quality and personal health
11. Time management strategies can mitigate stress
12. Institutional support is crucial for faculty well-being

#### Rule-Based Reasoning Process

**Step 1: Read Stress Level**
- Reads `stress_output.txt` from the ML component
- Parses the stress level (Low/Medium/High)
- Falls back to "Medium" if file not found

**Step 2: Apply Expert Rules**
The system has three main rule sets, one for each stress level:

##### HIGH STRESS RULE
**Conditions**: WSS 21-27, multiple high-intensity factors present
**Recommendations** (5 categories):
1. **Workload Adjustments**
   - Reduce subjects to 2-3
   - Negotiate smaller class sizes
   - Delegate administrative tasks
   - Request relief from committees

2. **Wellness Breaks**
   - 15-minute breaks every 2 hours
   - Complete day off weekly
   - 3-5 day wellness break within a month
   - Daily 30-minute physical activity

3. **Time Management**
   - Time-blocking for core activities
   - Batch similar tasks
   - Set meeting boundaries (max 2 hours/day)
   - Use preparation templates

4. **Sleep and Recovery**
   - Prioritize 7-8 hours sleep
   - Consistent sleep schedule
   - No work 2 hours before bedtime
   - Consider healthcare consultation

5. **Institutional Support**
   - Meet with department head
   - Request wellness resources
   - Explore sabbatical options
   - Document workload for review

##### MEDIUM STRESS RULE
**Conditions**: WSS 15-20, moderate workload intensity
**Recommendations** (5 categories):
1. **Time-Blocking Strategies**
2. **Work Cycle Monitoring**
3. **Efficiency Improvements**
4. **Wellness Maintenance**
5. **Preventive Planning**

##### LOW STRESS RULE
**Conditions**: WSS 9-14, balanced workload
**Recommendations** (5 categories):
1. **Routine Maintenance**
2. **Preventive Wellness Planning**
3. **Sustainable Growth**
4. **Long-Term Wellness**
5. **Institutional Contribution**

**Step 3: Explain Reasoning**
The system provides a reasoning explanation showing:
- Which rule was applied
- Conditions that were met
- Conclusion and rationale

### Output Format
The expert system displays:
1. **Knowledge Base Facts** (all 12 facts)
2. **Personalized Recommendations** (5 categories, 4 items each)
3. **Reasoning Explanation** (rule applied, conditions, conclusion)

---

## 3. How Both Components Operate Together

### System Architecture
This is a **hybrid AI system** combining:
- **Python ML Component**: Data-driven prediction
- **Visual Prolog Expert System**: Rule-based recommendations
- **Integration Script**: Orchestrates both components

### Communication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
│              (integration/run_system.py)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 1: ML COMPONENT                            │
│         (ml_component/stress_predictor.py)                   │
│                                                              │
│  1. User inputs 9 workload factors                          │
│  2. Calculate WSS (Workload Stress Score)                    │
│  3. Classify stress level (Low/Medium/High)                 │
│  4. Train/use Random Forest model (optional validation)      │
│  5. Write result to: integration/stress_output.txt           │
│     Format: STRESS_LEVEL=High                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ File: stress_output.txt
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 2: EXPERT SYSTEM                           │
│    (prolog_component/faculty_wellness/main.pro)              │
│                                                              │
│  1. Read stress_output.txt                                   │
│  2. Parse stress level                                       │
│  3. Apply expert rules (knowledge base + rules)              │
│  4. Generate personalized recommendations                    │
│  5. Display reasoning explanation                            │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Integration Process

#### Phase 1: ML Prediction
1. **User Input**: Faculty enters workload data via `run_system.py`
2. **Prediction**: `FacultyStressPredictor.predict_stress()` calculates:
   - WSS score (9-27)
   - Stress level category
   - Optional ML model prediction
3. **File Output**: Writes to `integration/stress_output.txt`:
   ```
   STRESS_LEVEL=High
   ```
4. **File Copy**: Also copies to `prolog_component/faculty_wellness/exe64/stress_output.txt` for Prolog executable

#### Phase 2: Expert System Processing
1. **File Reading**: Prolog reads `stress_output.txt` from multiple possible paths:
   - `stress_output.txt` (local directory)
   - `integration/stress_output.txt` (relative path)
   - `prolog_component/faculty_wellness/exe64/stress_output.txt` (executable directory)
2. **Parsing**: Extracts stress level using pattern matching:
   - Looks for `STRESS_LEVEL=Low`, `STRESS_LEVEL=Medium`, or `STRESS_LEVEL=High`
3. **Rule Application**: Matches stress level to appropriate rule:
   - `generateRecommendations("High")` → High stress recommendations
   - `generateRecommendations("Medium")` → Medium stress recommendations
   - `generateRecommendations("Low")` → Low stress recommendations
4. **Output Display**: Shows:
   - Knowledge base facts
   - Personalized recommendations (20 items total)
   - Reasoning explanation

### File-Based Communication
The components communicate via **text file** (`stress_output.txt`):
- **Format**: Simple key-value pair
- **Location**: Multiple paths checked for portability
- **Advantages**: 
  - Language-independent
  - Simple and reliable
  - No complex inter-process communication needed
  - Works across different platforms

### Error Handling
- **If file not found**: Prolog defaults to "Medium" stress
- **If parsing fails**: Prolog shows "Unknown" stress level
- **If ML component fails**: User can manually create `stress_output.txt`

### Running the Complete System

**Option 1: Integrated Menu** (Recommended)
```bash
python integration/run_system.py
```
- Menu-driven interface
- Handles both components automatically
- Option to run Prolog after prediction

**Option 2: Separate Execution**
```bash
# Step 1: Run ML component
python ml_component/predict.py

# Step 2: Run Prolog component
prolog_component/faculty_wellness/exe64/faculty_wellness.exe
```

### Key Benefits of Hybrid Approach
1. **Accuracy**: ML model learns patterns from data
2. **Interpretability**: WSS provides transparent scoring
3. **Expertise**: Prolog rules encode domain knowledge
4. **Flexibility**: Can update rules without retraining model
5. **Portability**: File-based communication works across platforms

---

## Summary

1. **Stress Prediction**: Uses WSS calculation (9 factors → 9-27 score → Low/Medium/High) with ML model support
2. **Recommendations**: Rule-based expert system applies knowledge base facts and expert rules to generate 20 personalized recommendations per stress level
3. **Integration**: File-based communication (`stress_output.txt`) allows Python ML and Visual Prolog expert system to work together seamlessly

