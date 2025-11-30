"""
AI-Powered Faculty Stress Detector - Machine Learning Component
This module predicts faculty stress levels based on workload factors.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
import pickle
import os


class FacultyStressPredictor:
    """Predicts faculty stress levels using Workload Stress Score (WSS) calculation."""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'subjects_handled', 'students_total', 'prep_hours',
            'research_load_hours', 'committee_duties', 'admin_tasks',
            'meeting_hours', 'sleep_hours', 'weekend_work'
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
        if row['students_total'] < 60:
            wss += 1
        elif row['students_total'] <= 100:
            wss += 2
        else:
            wss += 3
        
        # Preparation Hours: <6=1, 6-10=2, >10=3
        if row['prep_hours'] < 6:
            wss += 1
        elif row['prep_hours'] <= 10:
            wss += 2
        else:
            wss += 3
        
        # Research Load: <4=1, 4-6=2, >6=3
        if row['research_load_hours'] < 4:
            wss += 1
        elif row['research_load_hours'] <= 6:
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
        if row['admin_tasks'] <= 1:
            wss += 1
        elif row['admin_tasks'] <= 3:
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
        if row['weekend_work'] == 0:
            wss += 1
        elif row['weekend_work'] <= 2:
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
            
            # Check if we need to drop faculty_id column
            if 'faculty_id' in df.columns:
                df = df.drop('faculty_id', axis=1)
            elif 'Faculty_ID' in df.columns:
                df = df.drop('Faculty_ID', axis=1)
            
            # Ensure we have exactly the right columns in the right order
            expected_cols = self.feature_names
            actual_cols = list(df.columns)
            
            if actual_cols != expected_cols:
                print(f"Adjusting column names to match expected format...")
                print(f"Expected: {expected_cols}")
                print(f"Found: {actual_cols}")
                
                # Verify we have the right number of columns
                if len(actual_cols) == len(expected_cols):
                    # Rename columns to match expected names
                    df.columns = expected_cols
                    print("✓ Columns renamed successfully")
                else:
                    raise ValueError(f"Column count mismatch. Expected {len(expected_cols)}, got {len(actual_cols)}")
            else:
                print("✓ Column names match expected format")
            
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
        
        # Check class distribution
        class_counts = y.value_counts()
        print(f"Class distribution: {dict(class_counts)}")
        
        # Adjust test size based on smallest class
        min_class_size = class_counts.min()
        test_size = max(0.15, min(0.3, min_class_size / len(df)))  # Ensure at least 1 sample per class in test
        
        # Split data with stratification
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
        except ValueError:
            # If stratification fails, use regular split
            print("Warning: Stratification failed, using regular split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        # Store test data for evaluation
        self.X_test = X_test
        self.y_test = y_test
        self.X_train = X_train
        self.y_train = y_train
        
        # Train Random Forest Classifier with balanced parameters
        self.model = RandomForestClassifier(
            n_estimators=200, 
            random_state=42,
            class_weight='balanced',  # Handle class imbalance
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2%}")
        print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        return self.model
    
    def evaluate_model_performance(self, df=None):
        """Evaluate model performance and return metrics including confusion matrix.
        
        Args:
            df: Optional DataFrame. If provided and test data not available, 
                will split data and evaluate. If None, uses stored test data.
        """
        if self.model is None:
            print("Error: Model not loaded or trained.")
            return None
        
        # If test data not available, try to recreate it from provided dataframe
        if not hasattr(self, 'X_test') or not hasattr(self, 'y_test'):
            if df is None:
                print("Error: Test data not available. Please provide dataset or retrain model.")
                return None
            
            # Recreate test split
            X = df[self.feature_names]
            y = df['stress_level']
            
            class_counts = y.value_counts()
            min_class_size = class_counts.min()
            test_size = max(0.15, min(0.3, min_class_size / len(df)))
            
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42, stratify=y
                )
            except ValueError:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
            
            self.X_test = X_test
            self.y_test = y_test
            self.X_train = X_train
            self.y_train = y_train
        
        # Get predictions
        y_pred = self.model.predict(self.X_test)
        y_train_pred = self.model.predict(self.X_train)
        
        # Calculate metrics
        test_accuracy = accuracy_score(self.y_test, y_pred)
        train_accuracy = accuracy_score(self.y_train, y_train_pred)
        
        # Get unique classes in order
        classes = sorted(list(set(list(self.y_test) + list(y_pred))))
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred, labels=classes)
        
        # Per-class metrics
        precision = precision_score(self.y_test, y_pred, labels=classes, average=None, zero_division=0)
        recall = recall_score(self.y_test, y_pred, labels=classes, average=None, zero_division=0)
        f1 = f1_score(self.y_test, y_pred, labels=classes, average=None, zero_division=0)
        
        # Overall metrics
        macro_precision = precision_score(self.y_test, y_pred, average='macro', zero_division=0)
        macro_recall = recall_score(self.y_test, y_pred, average='macro', zero_division=0)
        macro_f1 = f1_score(self.y_test, y_pred, average='macro', zero_division=0)
        weighted_f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)
        
        return {
            'test_accuracy': test_accuracy,
            'train_accuracy': train_accuracy,
            'confusion_matrix': cm,
            'classes': classes,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'macro_precision': macro_precision,
            'macro_recall': macro_recall,
            'macro_f1': macro_f1,
            'weighted_f1': weighted_f1,
            'test_samples': len(self.y_test),
            'train_samples': len(self.y_train)
        }
    
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
            # Note: Test data not available when loading from file
            # User needs to retrain or load dataset to evaluate performance


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
        'students_total': 110,
        'prep_hours': 9,
        'research_load_hours': 5,
        'committee_duties': 2,
        'admin_tasks': 3,
        'meeting_hours': 6,
        'sleep_hours': 6,
        'weekend_work': 2
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


