"""
Dataset Generator Script
Creates a sample dataset.xlsx file with 200-300 faculty records
if the dataset doesn't exist or needs to be regenerated.
"""

import pandas as pd
import numpy as np
import os


def generate_dataset(num_records=250, output_file='dataset.xlsx'):
    """Generate a synthetic faculty workload dataset."""
    
    np.random.seed(42)  # For reproducibility
    
    data = []
    
    for i in range(1, num_records + 1):
        faculty_id = f"F{i:03d}"
        
        # Generate realistic workload data
        subjects = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.1])
        students = np.random.randint(20, 200)
        prep_hours = np.random.randint(3, 15)
        research = np.random.randint(0, 12)
        committee = np.random.choice([0, 1, 2, 3, 4], p=[0.2, 0.3, 0.3, 0.15, 0.05])
        admin = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.15, 0.25, 0.25, 0.2, 0.1, 0.05])
        meetings = np.random.randint(0, 10)
        sleep = np.random.choice([4, 5, 6, 7, 8, 9], p=[0.05, 0.1, 0.2, 0.3, 0.25, 0.1])
        weekend = np.random.choice([0, 1, 2, 3, 4, 5, 6], p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.05, 0.05])
        
        data.append({
            'Faculty_ID': faculty_id,
            'subjects_handled': subjects,
            'total_students': students,
            'preparation_hours': prep_hours,
            'research_load': research,
            'committee_duties': committee,
            'administrative_tasks': admin,
            'meeting_hours': meetings,
            'sleep_hours': sleep,
            'weekend_work_frequency': weekend
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Dataset generated: {output_file}")
    print(f"Total records: {len(df)}")
    print(f"\nSample data:")
    print(df.head(10).to_string())
    print(f"\nDataset statistics:")
    print(df.describe())
    
    return df


if __name__ == "__main__":
    # Check if dataset exists
    if os.path.exists('dataset.xlsx'):
        response = input("dataset.xlsx already exists. Regenerate? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing dataset.")
            exit(0)
    
    print("Generating faculty workload dataset...")
    generate_dataset(num_records=250)
    print("\n✓ Dataset generation complete!")




