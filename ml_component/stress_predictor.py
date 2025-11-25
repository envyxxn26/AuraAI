"""
AI-Powered Faculty Stress Detector - Machine Learning Component
This module predicts faculty stress levels based on workload factors.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os


class FacultyStressPredictor:
    """Predicts faculty stress levels using Workload Stress Score (WSS) calculation."""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'subjects_handled', 'total_students', 'preparation_hours',
            'research_load', 'committee_duties', 'administrative_tasks',
            'meeting_hours', 'sleep_hours', 'weekend_work_frequency'
        ]
    
    def calculate_wss(self, row):
        """
        Calculate Workload Stress Score (WSS) based on the formula provided.
        Returns a score between 9-27.
        """
        wss = 0
        
        # Subjects Handled: 1-2=1pt, 3-4=2pts, 5+=3pts
        if row['subjects_handled'] <= 2:
            wss += 1
        elif row['subjects_handled'] <= 4:
            wss += 2
        else:
            wss += 3
        
        # Total Students: <60=1, 60-100=2, >100=3
        if row['total_students'] < 60:
            wss += 1
        elif row['total_students'] <= 100:
            wss += 2
        else:
            wss += 3
        
        # Preparation Hours: <6=1, 6-10=2, >10=3
        if row['preparation_hours'] < 6:
            wss += 1
        elif row['preparation_hours'] <= 10:
            wss += 2
        else:
            wss += 3
        
        # Research Load: <4=1, 4-6=2, >6=3
        if row['research_load'] < 4:
            wss += 1
        elif row['research_load'] <= 6:
            wss += 2
        else:
            wss += 3
        
        # Committee Duties: 0-1=1, 2=2, 3+=3
        if row['committee_duties'] <= 1:
            wss += 1
        elif row['committee_duties'] == 2:
            wss += 2
        else:
            wss += 3
        
        # Administrative Tasks: 0-1=1, 2-3=2, 4+=3
        if row['administrative_tasks'] <= 1:
            wss += 1
        elif row['administrative_tasks'] <= 3:
            wss += 2
        else:
            wss += 3
        
        # Meeting Hours: <3=1, 3-6=2, >6=3
        if row['meeting_hours'] < 3:
            wss += 1
        elif row['meeting_hours'] <= 6:
            wss += 2
        else:
            wss += 3
        
        # Sleep Hours: 7+=1, 6=2, <6=3
        if row['sleep_hours'] >= 7:
            wss += 1
        elif row['sleep_hours'] == 6:
            wss += 2
        else:
            wss += 3
        
        # Weekend Work Frequency: 0=1, 1-2=2, 3+=3
        if row['weekend_work_frequency'] == 0:
            wss += 1
        elif row['weekend_work_frequency'] <= 2:
            wss += 2
        else:
            wss += 3
        
        return wss
    
    def wss_to_stress_level(self, wss):
        """Convert WSS to stress level category."""
        if wss <= 14:
            return "Low"
        elif wss <= 20:
            return "Medium"
        else:
            return "High"
    
    def load_and_preprocess_data(self, filepath):
        """Load dataset and preprocess it."""
        try:
            # Read Excel file
            df = pd.read_excel(filepath)
            
            # Check if we need to set column names
            if df.columns[0] == 'Faculty_ID' or 'Faculty_ID' in df.columns:
                # Dataset already has headers
                if 'Faculty_ID' in df.columns:
                    df = df.drop('Faculty_ID', axis=1)
            else:
                # Set column names if not present
                df.columns = self.feature_names
            
            # Ensure we have the right number of columns
            if len(df.columns) != len(self.feature_names):
                df.columns = self.feature_names[:len(df.columns)]
            
            # Calculate WSS for each row
            df['wss'] = df.apply(self.calculate_wss, axis=1)
            
            # Convert WSS to stress level
            df['stress_level'] = df['wss'].apply(self.wss_to_stress_level)
            
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def train_model(self, df):
        """Train a Random Forest model for stress prediction."""
        # Prepare features and target
        X = df[self.feature_names]
        y = df['stress_level']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest Classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return self.model
    
    def predict_stress(self, faculty_data):
        """
        Predict stress level for a single faculty member.
        faculty_data should be a dictionary or list with 9 values.
        """
        if isinstance(faculty_data, dict):
            # Convert dict to DataFrame
            df_input = pd.DataFrame([faculty_data])
        elif isinstance(faculty_data, list):
            # Convert list to DataFrame
            df_input = pd.DataFrame([faculty_data], columns=self.feature_names)
        else:
            raise ValueError("faculty_data must be dict or list")
        
        # Calculate WSS
        wss = self.calculate_wss(df_input.iloc[0])
        
        # Get stress level
        stress_level = self.wss_to_stress_level(wss)
        
        # Also use model prediction if available
        if self.model:
            model_prediction = self.model.predict(df_input)[0]
            return {
                'wss': int(wss),
                'stress_level': stress_level,
                'model_prediction': model_prediction
            }
        else:
            return {
                'wss': int(wss),
                'stress_level': stress_level
            }
    
    def save_model(self, filepath='ml_component/stress_model.pkl'):
        """Save the trained model."""
        if self.model:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='ml_component/stress_model.pkl'):
        """Load a trained model."""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded from {filepath}")


def write_stress_output(stress_level, output_file='integration/stress_output.txt'):
    """Write stress level prediction to output file for Prolog system."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(f"STRESS_LEVEL={stress_level}\n")
    print(f"Stress level written to {output_file}")


def main():
    """Main function to run the ML component."""
    print("=" * 60)
    print("AI-Powered Faculty Stress Detector - ML Component")
    print("=" * 60)
    
    # Initialize predictor
    predictor = FacultyStressPredictor()
    
    # Load and preprocess data
    print("\n[1] Loading dataset...")
    df = predictor.load_and_preprocess_data('dataset.xlsx')
    
    if df is None:
        print("Failed to load dataset. Exiting.")
        return
    
    print(f"Dataset loaded: {len(df)} records")
    print(f"\nStress Level Distribution:")
    print(df['stress_level'].value_counts())
    
    # Train model
    print("\n[2] Training model...")
    predictor.train_model(df)
    
    # Save model
    print("\n[3] Saving model...")
    predictor.save_model()
    
    # Example prediction
    print("\n[4] Running example prediction...")
    example_faculty = {
        'subjects_handled': 4,
        'total_students': 110,
        'preparation_hours': 9,
        'research_load': 5,
        'committee_duties': 2,
        'administrative_tasks': 3,
        'meeting_hours': 6,
        'sleep_hours': 6,
        'weekend_work_frequency': 2
    }
    
    result = predictor.predict_stress(example_faculty)
    print(f"\nExample Faculty Prediction:")
    print(f"  WSS Score: {result['wss']}")
    print(f"  Stress Level: {result['stress_level']}")
    
    # Write output for Prolog system
    write_stress_output(result['stress_level'])
    
    print("\n" + "=" * 60)
    print("ML Component execution completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

