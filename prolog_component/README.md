# Visual Prolog Expert System Component

## Overview

This directory contains the Visual Prolog expert system that generates personalized wellness recommendations based on stress levels predicted by the Python ML component.

## File

- `faculty_wellness.pro` - Main Prolog program with knowledge base and rules

## Knowledge Base

The system contains:
- **12 Facts**: About faculty wellness and workload patterns
- **6+ Rules**: Mapping stress levels to specific recommendations

## How to Use

### Using Visual Prolog IDE

1. Open Visual Prolog IDE
2. Create a new console application project
3. Copy the contents of `faculty_wellness.pro` into your main project file
4. Build the project (F7)
5. Run the project (F5)

### File Dependencies

The system reads from: `integration/stress_output.txt`

Make sure this file exists and contains:
```
STRESS_LEVEL=High
```
(or `Medium` or `Low`)

## Output

The system will:
1. Read the stress level from the output file
2. Display knowledge base facts
3. Apply expert rules
4. Generate personalized recommendations
5. Explain the reasoning

## Customization

To add new rules or facts:

1. Add facts using the `fact/2` predicate
2. Add rules by creating new `generateRecommendations/1` clauses
3. Update `explainReasoning/1` for new reasoning explanations

## Example Output

```
============================================================
AI-Powered Faculty Stress Detector - Expert System
Wellness Recommendation System
============================================================

Stress Level Detected: Medium

Analyzing workload patterns and wellness indicators...

Knowledge Base Facts:
-------------------
[Displays all facts]

Applying Expert Rules...

============================================================
PERSONALIZED WELLNESS RECOMMENDATIONS
============================================================

STRESS LEVEL: MEDIUM
-------------------

PREVENTIVE MEASURES RECOMMENDED:

1. TIME-BLOCKING STRATEGIES:
   ...
```

## Notes

- The file path in the code uses Windows-style paths (`\\`)
- Adjust paths if running on Linux/Mac
- Ensure the output file is in the correct location relative to the Prolog executable

