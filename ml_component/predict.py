"""
Standalone prediction script for individual faculty members.
Usage: python predict.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stress_predictor import FacultyStressPredictor, write_stress_output


def get_faculty_input():
    """Get faculty workload data from user input."""
    print("\nEnter Faculty Workload Information:")
    print("-" * 40)
    
    try:
        # Add input validation and default values for testing
        subjects = int(input("Number of subjects handled (1-10) [default: 4]: ") or "4")
        students = int(input("Total number of students [default: 110]: ") or "110")
        prep_hours = int(input("Preparation hours per week [default: 9]: ") or "9")
        research = int(input("Research load (hours per week) [default: 5]: ") or "5")
        committee = int(input("Committee duties (count) [default: 2]: ") or "2")
        admin = int(input("Administrative tasks (count) [default: 3]: ") or "3")
        meetings = int(input("Meeting hours per week [default: 6]: ") or "6")
        sleep = int(input("Sleep hours per night [default: 6]: ") or "6")
        weekend = int(input("Weekend work frequency (times per month) [default: 2]: ") or "2")
        
        # Validate ranges
        if not (1 <= subjects <= 10):
            print("Warning: Subjects should be between 1-10")
        if not (20 <= students <= 300):
            print("Warning: Students should be between 20-300")
        if not (1 <= prep_hours <= 20):
            print("Warning: Prep hours should be between 1-20")
        if not (0 <= research <= 15):
            print("Warning: Research hours should be between 0-15")
        if not (4 <= sleep <= 10):
            print("Warning: Sleep hours should be between 4-10")
        
        return {
            'subjects_handled': subjects,
            'students_total': students,
            'prep_hours': prep_hours,
            'research_load_hours': research,
            'committee_duties': committee,
            'admin_tasks': admin,
            'meeting_hours': meetings,
            'sleep_hours': sleep,
            'weekend_work': weekend
        }
    except (ValueError, EOFError) as e:
        print(f"Error: {e}")
        print("Using default values for testing...")
        return {
            'subjects_handled': 4,
            'students_total': 110,
            'prep_hours': 9,
            'research_load_hours': 5,
            'committee_duties': 2,
            'admin_tasks': 3,
            'meeting_hours': 6,
            'sleep_hours': 6,
            'weekend_work': 2
        }


def main():
    """Main prediction interface."""
    print("=" * 60)
    print("Faculty Stress Level Predictor")
    print("=" * 60)
    
    # Initialize predictor
    predictor = FacultyStressPredictor()
    
    # Try to load existing model
    try:
        predictor.load_model()
    except:
        print("Note: No pre-trained model found. Using WSS calculation only.")
    
    # Get input
    faculty_data = get_faculty_input()
    
    if faculty_data is None:
        print("Invalid input. Exiting.")
        sys.exit(1)
    
    # Predict
    print("\n" + "=" * 60)
    print("Calculating Stress Level...")
    print("=" * 60)
    
    result = predictor.predict_stress(faculty_data)
    
    # Display results
    print(f"\nWorkload Stress Score (WSS): {result['wss']}/27")
    print(f"Predicted Stress Level: {result['stress_level']} Stress")
    
    # Write output for Prolog
    write_stress_output(result['stress_level'])
    
    print("\n" + "=" * 60)
    print("Prediction complete! Output written to integration/stress_output.txt")
    print("=" * 60)
    print("\nYou can now run the Visual Prolog expert system to get recommendations.")


if __name__ == "__main__":
    main()

