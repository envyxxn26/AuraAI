"""
Integration script to run the complete hybrid AI system.
This script coordinates the Python ML component and Visual Prolog expert system.
"""

import os
import sys
import subprocess
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml_component.stress_predictor import FacultyStressPredictor, write_stress_output


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("AI-Powered Faculty Stress Detector")
    print("Hybrid AI System - Main Menu")
    print("=" * 60)
    print("\nSYSTEM OPTIONS:")
    print("1. Enter new faculty data for prediction")
    print("2. Select faculty from dataset")
    print("3. Batch analyze entire dataset")
    print("4. View model performance")
    print("5. Exit")
    print("=" * 60)


def get_faculty_input():
    """Get faculty workload information from user."""
    print("\nEnter Faculty Workload Information:")
    print("-" * 40)
    print("(Press Enter to use default values shown in brackets)")
    
    try:
        subjects = int(input("Number of subjects handled (1-10) [4]: ") or "4")
        students = int(input("Total number of students [110]: ") or "110")
        prep_hours = int(input("Preparation hours per week [9]: ") or "9")
        research = int(input("Research load (hours per week) [5]: ") or "5")
        committee = int(input("Committee duties (count) [2]: ") or "2")
        admin = int(input("Administrative tasks (count) [3]: ") or "3")
        meetings = int(input("Meeting hours per week [6]: ") or "6")
        sleep = int(input("Sleep hours per night [6]: ") or "6")
        weekend = int(input("Weekend work frequency (times per month) [2]: ") or "2")
        
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
        print(f"Input error: {e}")
        print("Using default values...")
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


def predict_single_faculty(predictor, faculty_data):
    """Predict stress for a single faculty member."""
    result = predictor.predict_stress(faculty_data)
    
    print(f"\n{'='*60}")
    print("PREDICTION RESULTS")
    print(f"{'='*60}")
    print(f"Workload Stress Score (WSS): {result['wss']}/27")
    print(f"Stress Level (WSS-based): {result['stress_level']} Stress")
    if 'model_prediction' in result:
        print(f"ML Model Prediction: {result['model_prediction']} Stress")
        # Note: We use WSS-based prediction as the primary result
        if result['model_prediction'] != result['stress_level']:
            print(f"Note: Model prediction differs from WSS-based prediction.")
    print(f"{'='*60}\n")
    
    # Write output - always use WSS-based stress level
    write_stress_output(result['stress_level'])
    
    # Also copy to Prolog executable directory
    prolog_exe_dir = Path("prolog_component/faculty_wellness/exe64")
    prolog_exe_dir.mkdir(parents=True, exist_ok=True)
    prolog_stress_file = prolog_exe_dir / "stress_output.txt"
    with open(prolog_stress_file, 'w') as f:
        f.write(f"STRESS_LEVEL={result['stress_level']}\n")
    
    return result['stress_level']


def select_faculty_from_dataset(predictor):
    """Allow user to select a faculty member from the dataset."""
    print("\n" + "=" * 60)
    print("Select Faculty from Dataset")
    print("=" * 60)
    print("Note: This option selects an existing faculty member from the dataset.")
    print("To enter custom data (like all zeros), use Option 1 instead.\n")
    
    # Load dataset
    df = predictor.load_and_preprocess_data('dataset.xlsx')
    if df is None:
        print("Error: Could not load dataset.")
        return None
    
    print(f"\nDataset contains {len(df)} faculty records.")
    print("\nFirst 10 records:")
    print(df.head(10).to_string())
    
    try:
        index = int(input(f"\nEnter faculty index (0-{len(df)-1}): "))
        if 0 <= index < len(df):
            faculty_data = df.iloc[index][predictor.feature_names].to_dict()
            print(f"\nSelected Faculty #{index}:")
            for key, value in faculty_data.items():
                print(f"  {key}: {value}")
            
            stress_level = predict_single_faculty(predictor, faculty_data)
            return stress_level
        else:
            print("Invalid index.")
            return None
    except (ValueError, EOFError):
        print("Invalid input.")
        return None


def batch_analyze_dataset(predictor):
    """Batch analyze the entire dataset."""
    print("\n" + "=" * 60)
    print("Batch Analyze Entire Dataset")
    print("=" * 60)
    
    # Load dataset
    df = predictor.load_and_preprocess_data('dataset.xlsx')
    if df is None:
        print("Error: Could not load dataset.")
        return
    
    print(f"\nAnalyzing {len(df)} faculty records...")
    
    # Analyze each record
    results = []
    for idx, row in df.iterrows():
        faculty_data = row[predictor.feature_names].to_dict()
        result = predictor.predict_stress(faculty_data)
        results.append({
            'index': idx,
            'wss': result['wss'],
            'stress_level': result['stress_level']
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("BATCH ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"\nTotal Records Analyzed: {len(results_df)}")
    print(f"\nStress Level Distribution:")
    print(results_df['stress_level'].value_counts())
    print(f"\nWSS Score Statistics:")
    print(results_df['wss'].describe())
    
    # Save results
    output_file = 'integration/batch_analysis_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    print("\n" + "=" * 60)


def view_model_performance(predictor):
    """Display model performance metrics including confusion matrix."""
    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE EVALUATION")
    print("=" * 60)
    
    # Check if model is trained
    if predictor.model is None:
        print("\nError: Model not trained. Please train the model first.")
        print("Loading or training model...")
        
        model_path = 'ml_component/stress_model.pkl'
        if os.path.exists(model_path):
            predictor.load_model()
        else:
            print("Training new model...")
            df = predictor.load_and_preprocess_data('dataset.xlsx')
            if df is None:
                print("Error: Could not load dataset.")
                return
            predictor.train_model(df)
            predictor.save_model()
    
    # Try to evaluate performance
    # If test data not available, load dataset to recreate test split
    if not hasattr(predictor, 'X_test'):
        print("Loading dataset to evaluate performance...")
        df = predictor.load_and_preprocess_data('dataset.xlsx')
        if df is None:
            print("Error: Could not load dataset for evaluation.")
            return
        metrics = predictor.evaluate_model_performance(df)
    else:
        metrics = predictor.evaluate_model_performance()
    
    if metrics is None:
        print("Error: Could not evaluate model performance.")
        return
    
    # Display metrics
    print(f"\n{'='*60}")
    print("OVERALL PERFORMANCE METRICS")
    print(f"{'='*60}")
    print(f"Test Accuracy:     {metrics['test_accuracy']:.2%}")
    print(f"Training Accuracy: {metrics['train_accuracy']:.2%}")
    print(f"Test Samples:      {metrics['test_samples']}")
    print(f"Training Samples:   {metrics['train_samples']}")
    
    print(f"\n{'='*60}")
    print("MACRO-AVERAGED METRICS")
    print(f"{'='*60}")
    print(f"Macro Precision:   {metrics['macro_precision']:.4f}")
    print(f"Macro Recall:      {metrics['macro_recall']:.4f}")
    print(f"Macro F1-Score:    {metrics['macro_f1']:.4f}")
    print(f"Weighted F1-Score: {metrics['weighted_f1']:.4f}")
    
    # Per-class metrics
    print(f"\n{'='*60}")
    print("PER-CLASS METRICS")
    print(f"{'='*60}")
    print(f"{'Class':<10} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 50)
    for i, cls in enumerate(metrics['classes']):
        print(f"{cls:<10} {metrics['precision'][i]:<12.4f} {metrics['recall'][i]:<12.4f} {metrics['f1'][i]:<12.4f}")
    
    # Confusion Matrix
    print(f"\n{'='*60}")
    print("CONFUSION MATRIX")
    print(f"{'='*60}")
    print("\nRows = Actual, Columns = Predicted\n")
    
    # Header
    header = "Actual \\ Predicted"
    print(f"{header:<20}", end="")
    for cls in metrics['classes']:
        print(f"{cls:>10}", end="")
    print()
    print("-" * (20 + len(metrics['classes']) * 10))
    
    # Matrix rows
    for i, actual_class in enumerate(metrics['classes']):
        print(f"{actual_class:<20}", end="")
        for j in range(len(metrics['classes'])):
            print(f"{metrics['confusion_matrix'][i][j]:>10}", end="")
        print()
    
    # Summary statistics from confusion matrix
    print(f"\n{'='*60}")
    print("CONFUSION MATRIX SUMMARY")
    print(f"{'='*60}")
    total = metrics['confusion_matrix'].sum()
    correct = metrics['confusion_matrix'].trace()
    print(f"Total Predictions:  {total}")
    print(f"Correct Predictions: {correct}")
    print(f"Incorrect Predictions: {total - correct}")
    print(f"Accuracy: {correct/total:.2%}")
    
    print("\n" + "=" * 60)


def run_prolog_component(stress_level):
    """Run the Visual Prolog expert system."""
    print("\n" + "=" * 60)
    print("STEP 2: Running Expert System Component")
    print("=" * 60)
    
    # Try to run the Prolog executable with command-line argument
    prolog_exe = Path("prolog_component/faculty_wellness/exe64/faculty_wellness.exe")
    
    if prolog_exe.exists():
        print(f"\nRunning Prolog expert system with stress level: {stress_level}")
        try:
            result = subprocess.run(
                [str(prolog_exe), f"--stress={stress_level}"],
                cwd=str(prolog_exe.parent),
                timeout=30
            )
            print("\n+ Prolog component completed!")
            return True
        except subprocess.TimeoutExpired:
            print("\n+ Prolog component timed out (this is normal if waiting for input)")
            return True
        except Exception as e:
            print(f"\nWarning: Could not run Prolog executable: {e}")
            print("You can manually run it with:")
            print(f'  {prolog_exe} --stress={stress_level}')
    else:
        print("\nNote: Prolog executable not found. Please:")
        print("1. Open Visual Prolog IDE")
        print("2. Load the project: prolog_component/faculty_wellness")
        print("3. Build the project (Ctrl+Shift+B)")
        print("4. Run it manually with:")
        print(f'   faculty_wellness.exe --stress={stress_level}')
        print("\nOr run from Visual Prolog IDE and pass the stress level as argument.")
    
    print("=" * 60)


def initialize_predictor():
    """Initialize and load/train the predictor model."""
    predictor = FacultyStressPredictor()
    
    # Try to load existing model
    model_path = 'ml_component/stress_model.pkl'
    if os.path.exists(model_path):
        predictor.load_model()
        print("+ Loaded pre-trained model.")
    else:
        print("No pre-trained model found. Training new model...")
        # Load and train
        df = predictor.load_and_preprocess_data('dataset.xlsx')
        if df is not None:
            predictor.train_model(df)
            predictor.save_model()
        else:
            print("Error: Could not load dataset for training.")
            return None
    
    return predictor


def main():
    """Main integration function with menu system."""
    print("\n" + "=" * 60)
    print("AI-Powered Faculty Stress Detector")
    print("Hybrid AI System - Integration Script")
    print("=" * 60)
    
    # Initialize predictor
    predictor = initialize_predictor()
    if predictor is None:
        print("Failed to initialize predictor. Exiting.")
        return
    
    while True:
        display_menu()
        
        try:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                # Enter new faculty data for prediction
                faculty_data = get_faculty_input()
                stress_level = predict_single_faculty(predictor, faculty_data)
                
                # Ask if user wants to run Prolog
                run_prolog = input("\nRun Prolog expert system? (y/n): ").strip().lower()
                if run_prolog == 'y':
                    run_prolog_component(stress_level)
            
            elif choice == '2':
                # Select faculty from dataset
                stress_level = select_faculty_from_dataset(predictor)
                
                if stress_level:
                    # Ask if user wants to run Prolog
                    run_prolog = input("\nRun Prolog expert system? (y/n): ").strip().lower()
                    if run_prolog == 'y':
                        run_prolog_component(stress_level)
            
            elif choice == '3':
                # Batch analyze entire dataset
                batch_analyze_dataset(predictor)
            
            elif choice == '4':
                # View model performance
                view_model_performance(predictor)
            
            elif choice == '5':
                # Exit
                print("\nThank you for using the AI-Powered Faculty Stress Detector!")
                print("Exiting...")
                break
            
            else:
                print("\nInvalid option. Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
