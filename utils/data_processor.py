import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from config import *
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.label_encoders = {}
        # Initialize label encoder for Health_Outcome
        self.label_encoders['Health_Outcome'] = LabelEncoder()
        # Fit the encoder with possible health outcomes
        self.label_encoders['Health_Outcome'].fit([
            'Healthy', 'Minor Issue', 'Requires Treatment', 'Critical', 'Emergency'
        ])
        
    def load_data(self):
        """Load or generate sample data"""
        try:
            return pd.read_csv(DATASET_PATH)
        except FileNotFoundError:
            print("Dataset not found. Creating sample data...")
            # Create sample data
            np.random.seed(42)
            n_samples = 1000

            data = {
                'Animal_ID': [f'A{i:04d}' for i in range(n_samples)],
                'Species': np.random.choice(['Dog', 'Cat', 'Horse', 'Parrot', 'Snake'], n_samples),
                'Age': np.random.uniform(0, 15, n_samples),
                'Gender': np.random.choice(['Male', 'Female'], n_samples),
                'Weight': np.random.uniform(1, 100, n_samples),
                'Heart_Rate': np.random.uniform(60, 200, n_samples),
                'Respiratory_Rate': np.random.uniform(10, 40, n_samples),
                'Temperature': np.random.uniform(35, 42, n_samples),
                'Diet_Type': np.random.choice(['Balanced', 'Poor', 'Excellent'], n_samples),
                'Habitat_Quality': np.random.choice(['Good', 'Average', 'Poor'], n_samples),
                'Genetic_Risk': np.random.choice(['Low', 'Medium', 'High'], n_samples),
                'Medical_History': np.random.choice(['None', 'Healthy', 'Chronic', 'Surgery'], n_samples),
                'Health_Outcome': np.random.choice([
                    'Healthy', 'Minor Issue', 'Requires Treatment', 'Critical', 'Emergency'
                ], n_samples)
            }
            
            df = pd.DataFrame(data)
            df.to_csv(DATASET_PATH, index=False)
            return df
            
    def preprocess_data(self, df):
        """Preprocess the data"""
        try:
            df_processed = df.copy()
            
            # Handle numerical columns
            numerical_columns = ['Age', 'Weight', 'Heart_Rate', 'Respiratory_Rate', 'Temperature']
            for col in numerical_columns:
                if col in df_processed.columns:
                    df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
                    mean_val = df_processed[col].mean()
                    df_processed[col] = df_processed[col].fillna(mean_val)
            
            # Handle categorical columns
            categorical_columns = [
                'Species', 'Gender', 'Diet_Type', 'Habitat_Quality', 
                'Genetic_Risk', 'Medical_History'
            ]
            
            for col in categorical_columns:
                if col in df_processed.columns:
                    if col not in self.label_encoders:
                        self.label_encoders[col] = LabelEncoder()
                        df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col].astype(str))
                    else:
                        try:
                            df_processed[col] = self.label_encoders[col].transform(df_processed[col].astype(str))
                        except ValueError:
                            # Handle unseen categories by refitting
                            self.label_encoders[col] = LabelEncoder()
                            df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col].astype(str))
            
            # Drop any non-feature columns that might have been added
            columns_to_drop = ['Symptoms', 'Animal_ID']
            df_processed = df_processed.drop(columns=[col for col in columns_to_drop if col in df_processed.columns])
            
            return df_processed
            
        except Exception as e:
            logger.error(f"Error in preprocess_data: {str(e)}")
            raise
        
    def prepare_data_for_training(self, df):
        """Prepare data for model training"""
        try:
            df_processed = self.preprocess_data(df)
            
            if 'Health_Outcome' in df_processed.columns:
                # Encode target variable
                y = self.label_encoders['Health_Outcome'].transform(df_processed['Health_Outcome'].astype(str))
                
                # Prepare features
                X = df_processed.drop(['Health_Outcome'], axis=1, errors='ignore')
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
                )
                
                return X_train, X_test, y_train, y_test
            else:
                # For prediction data without Health_Outcome
                return df_processed
                
        except Exception as e:
            logger.error(f"Error in prepare_data_for_training: {str(e)}")
            raise