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
        subjects = int(input("Number of subjects handled (1-10): "))
        students = int(input("Total number of students: "))
        prep_hours = int(input("Preparation hours per week: "))
        research = int(input("Research load (hours per week): "))
        committee = int(input("Committee duties (count): "))
        admin = int(input("Administrative tasks (count): "))
        meetings = int(input("Meeting hours per week: "))
        sleep = int(input("Sleep hours per night: "))
        weekend = int(input("Weekend work frequency (times per month): "))
        
        return {
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
    except ValueError:
        print("Error: Please enter valid numbers.")
        return None


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

