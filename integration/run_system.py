"""
Integration script to run the complete hybrid AI system.
This script coordinates the Python ML component and Visual Prolog expert system.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml_component.stress_predictor import FacultyStressPredictor, write_stress_output


def run_ml_component():
    """Run the Python ML component."""
    print("=" * 60)
    print("STEP 1: Running Machine Learning Component")
    print("=" * 60)
    
    # Initialize predictor
    predictor = FacultyStressPredictor()
    
    # Try to load existing model
    model_path = 'ml_component/stress_model.pkl'
    if os.path.exists(model_path):
        predictor.load_model()
        print("Loaded pre-trained model.")
    else:
        print("No pre-trained model found. Training new model...")
        # Load and train
        df = predictor.load_and_preprocess_data('dataset.xlsx')
        if df is not None:
            predictor.train_model(df)
            predictor.save_model()
    
    # Get faculty input
    print("\nEnter Faculty Workload Information:")
    print("-" * 40)
    
    try:
        subjects = int(input("Number of subjects handled (1-10): "))
        students = int(input("Total number of students: "))
        prep_hours = int(input("Preparation hours per week: "))
        research = int(input("Research load (hours per week): "))
        committee = int(input("Committee duties (count): "))
        admin = int(input("Administrative tasks (count): "))
        meetings = int(input("Meeting hours per week: "))
        sleep = int(input("Sleep hours per night: "))
        weekend = int(input("Weekend work frequency (times per month): "))
        
        faculty_data = {
            'subjects_handled': subjects,
            'total_students': students,
            'preparation_hours': prep_hours,
            'research_load': research,
            'committee_duties': committee,
            'administrative_tasks': admin,
            'meeting_hours': meetings,
            'sleep_hours': sleep,
            'weekend_work_frequency': weekend
        }
        
        # Predict
        result = predictor.predict_stress(faculty_data)
        
        print(f"\nWorkload Stress Score (WSS): {result['wss']}/27")
        print(f"Predicted Stress Level: {result['stress_level']} Stress")
        
        # Write output
        write_stress_output(result['stress_level'])
        
        print("\n✓ ML Component completed successfully!")
        return True
        
    except ValueError:
        print("Error: Invalid input. Please enter valid numbers.")
        return False
    except Exception as e:
        print(f"Error in ML component: {e}")
        return False


def run_prolog_component():
    """Run the Visual Prolog expert system."""
    print("\n" + "=" * 60)
    print("STEP 2: Running Expert System Component")
    print("=" * 60)
    print("\nNote: To run the Visual Prolog expert system, please:")
    print("1. Open Visual Prolog IDE")
    print("2. Load the project: prolog_component/faculty_wellness.pro")
    print("3. Build and run the project")
    print("\nAlternatively, if you have Visual Prolog compiler installed:")
    print("  vip.exe faculty_wellness.pro")
    print("\nThe Prolog system will read from: integration/stress_output.txt")
    print("=" * 60)


def main():
    """Main integration function."""
    print("\n" + "=" * 60)
    print("AI-Powered Faculty Stress Detector")
    print("Hybrid AI System - Integration Script")
    print("=" * 60)
    
    # Run ML component
    success = run_ml_component()
    
    if success:
        # Run Prolog component instructions
        run_prolog_component()
        
        print("\n" + "=" * 60)
        print("Integration Complete!")
        print("=" * 60)
        print("\nThe system has:")
        print("1. ✓ Predicted stress level using ML")
        print("2. → Written output to integration/stress_output.txt")
        print("3. → Ready for Prolog expert system processing")
        print("\nNext: Run the Visual Prolog expert system to get recommendations.")
    else:
        print("\nIntegration failed. Please check the errors above.")


if __name__ == "__main__":
    main()

