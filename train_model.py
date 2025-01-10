import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_data(df):
    """Prepare data for training with enhanced metrics"""
    
    # Create label encoders for categorical variables
    label_encoders = {}
    categorical_columns = [
        'Species', 'Breed', 'Diet_Type', 
        'Activity_Level', 'Living_Environment',
        'Vaccination_Status'
    ]
    
    for column in categorical_columns:
        label_encoders[column] = LabelEncoder()
        df[column] = label_encoders[column].fit_transform(df[column])
    
    # Split features and target
    X = df.drop(['Health_Status', 'Health_Score'], axis=1)
    y = df['Health_Status']
    
    # Save label encoders
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    return X, y

def train_model():
    """Train the enhanced health analysis model"""
    try:
        # Load data
        df = pd.read_csv('data/training_data.csv')
        logger.info(f"Loaded training data: {len(df)} samples")
        
        # Prepare data
        X, y = prepare_data(df)
        logger.info(f"Prepared data with {X.shape[1]} features")
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model with enhanced parameters
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        logger.info("\nModel Performance:")
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred))
        
        # Save model and scaler
        joblib.dump(model, 'models/health_analysis_model.pkl')
        joblib.dump(scaler, 'models/scaler.pkl')
        
        logger.info("Model and scaler saved successfully")
        
        # Save feature importances
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        feature_importance.to_csv('models/feature_importance.csv', index=False)
        logger.info("Feature importances saved to models/feature_importance.csv")
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

if __name__ == '__main__':
    train_model() 