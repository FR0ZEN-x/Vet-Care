import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(n_samples=1000):
    """Generate synthetic training data"""
    
    # Basic Information
    species = ['Dog', 'Cat', 'Horse', 'Bird', 'Reptile']
    breeds = {
        'Dog': ['Labrador', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Poodle'],
        'Cat': ['Persian', 'Siamese', 'Maine Coon', 'Bengal', 'Ragdoll'],
        'Horse': ['Arabian', 'Thoroughbred', 'Quarter Horse', 'Appaloosa'],
        'Bird': ['Parakeet', 'Cockatiel', 'Macaw', 'African Grey'],
        'Reptile': ['Bearded Dragon', 'Ball Python', 'Green Iguana', 'Leopard Gecko']
    }
    
    # Health Indicators
    diet_types = ['Premium Commercial', 'Basic Commercial', 'Home-Prepared', 'Raw Diet', 'Prescription']
    activity_levels = ['Very Active', 'Active', 'Moderate', 'Sedentary']
    living_environments = ['Indoor Only', 'Outdoor Only', 'Mixed', 'Controlled Environment']
    vaccination_status = ['Up to Date', 'Partially Vaccinated', 'Overdue', 'Not Vaccinated']
    
    # Generate base data
    data = {
        'Species': np.random.choice(species, n_samples),
        'Age': np.random.uniform(0, 20, n_samples),
        'Weight': np.random.uniform(1, 100, n_samples),
        'Diet_Type': np.random.choice(diet_types, n_samples),
        'Activity_Level': np.random.choice(activity_levels, n_samples),
        'Living_Environment': np.random.choice(living_environments, n_samples),
        'Vaccination_Status': np.random.choice(vaccination_status, n_samples),
        'Heart_Rate': np.random.uniform(40, 200, n_samples),
        'Respiratory_Rate': np.random.uniform(8, 60, n_samples),
        'Temperature': np.random.uniform(35, 42, n_samples)
    }
    
    # Add breed information
    breeds_list = []
    for species_name in data['Species']:
        breeds_list.append(np.random.choice(breeds[species_name]))
    data['Breed'] = breeds_list
    
    # Generate health scores based on the data
    df = pd.DataFrame(data)
    df['Health_Score'] = calculate_health_scores(df)
    
    # Add health status based on score
    df['Health_Status'] = df['Health_Score'].apply(lambda x: 
        'Healthy' if x >= 90 else
        'Minor Issue' if x >= 75 else
        'Requires Treatment' if x >= 60 else
        'Critical'
    )
    
    return df

def calculate_health_scores(df):
    """Calculate health scores"""
    scores = np.zeros(len(df))
    scores += 100  # Start with perfect score
    
    # Deduct points based on various factors
    for idx, row in df.iterrows():
        # Age-related deductions
        if row['Age'] > 10:
            scores[idx] -= 5
        
        # Activity level adjustments
        activity_adjustments = {
            'Very Active': 5,
            'Active': 2,
            'Moderate': 0,
            'Sedentary': -5
        }
        scores[idx] += activity_adjustments[row['Activity_Level']]
        
        # Vaccination status deductions
        vacc_deductions = {
            'Up to Date': 0,
            'Partially Vaccinated': 5,
            'Overdue': 15,
            'Not Vaccinated': 20
        }
        scores[idx] -= vacc_deductions[row['Vaccination_Status']]
        
        # Environment deductions
        env_deductions = {
            'Indoor Only': 0,
            'Outdoor Only': 5,
            'Mixed': 2,
            'Controlled Environment': 0
        }
        scores[idx] -= env_deductions[row['Living_Environment']]
    
    return np.clip(scores, 0, 100)

if __name__ == '__main__':
    # Generate sample data
    df = generate_sample_data(n_samples=1000)
    
    # Save to CSV
    df.to_csv('data/training_data.csv', index=False)
    print("Enhanced sample data generated and saved to data/training_data.csv") 