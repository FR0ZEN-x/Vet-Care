import joblib
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from config import *
import logging

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        try:
            self.rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=RANDOM_STATE
            )
            self.xgb_model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=RANDOM_STATE
            )
            self.best_model = None
            self.species_specific_models = {}
            self.label_encoder = LabelEncoder()
        except Exception as e:
            logger.error(f"Error initializing ModelTrainer: {str(e)}")
            raise
        
    def train(self, X_train, y_train):
        """Train multiple models and select the best one"""
        # Convert X_train to DataFrame if it's not already
        if not isinstance(X_train, pd.DataFrame):
            X_train = pd.DataFrame(X_train)
        
        # Train Random Forest
        rf_scores = cross_val_score(self.rf_model, X_train, y_train, cv=5)
        self.rf_model.fit(X_train, y_train)
        
        # Train XGBoost
        xgb_scores = cross_val_score(self.xgb_model, X_train, y_train, cv=5)
        self.xgb_model.fit(X_train, y_train)
        
        # Select best model based on cross-validation scores
        if np.mean(rf_scores) > np.mean(xgb_scores):
            self.best_model = self.rf_model
            print("Selected Random Forest as best model")
        else:
            self.best_model = self.xgb_model
            print("Selected XGBoost as best model")
        
        # Train species-specific models if Species column exists
        if 'Species' in X_train.columns:
            # Create a DataFrame with both features and target
            train_data = X_train.copy()
            train_data['target'] = y_train
            
            # Group by species
            for species, group in train_data.groupby('Species'):
                if len(group) >= 50:  # Minimum samples threshold
                    species_model = RandomForestClassifier(
                        n_estimators=50,
                        max_depth=5,
                        random_state=RANDOM_STATE
                    )
                    # Split features and target
                    species_X = group.drop('target', axis=1)
                    species_y = group['target']
                    species_model.fit(species_X, species_y)
                    self.species_specific_models[species] = species_model
    
    def predict(self, X):
        """Make predictions using the appropriate model"""
        try:
            # Convert X to DataFrame if it's not already
            if not isinstance(X, pd.DataFrame):
                X = pd.DataFrame(X)
            
            if self.best_model is None:
                raise ValueError("Model not trained. Please train the model first.")
            
            predictions = []
            
            if 'Species' in X.columns and self.species_specific_models:
                # Use species-specific models where available
                for idx, row in X.iterrows():
                    species = row['Species']
                    if species in self.species_specific_models:
                        pred = self.species_specific_models[species].predict(row.to_frame().T)[0]
                    else:
                        pred = self.best_model.predict(row.to_frame().T)[0]
                    predictions.append(pred)
                return np.array(predictions)
            else:
                # Use best general model
                return self.best_model.predict(X)
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
    
    def evaluate(self, X_test, y_test):
        """Evaluate the model and save detailed metrics"""
        # Convert X_test to DataFrame if it's not already
        if not isinstance(X_test, pd.DataFrame):
            X_test = pd.DataFrame(X_test)
            
        y_pred = self.predict(X_test)
        
        metrics = {
            'overall': {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted')
            }
        }
        
        # Calculate species-specific metrics if Species column exists
        if 'Species' in X_test.columns:
            # Create a DataFrame with both features and target
            test_data = X_test.copy()
            test_data['target'] = y_test
            
            # Group by species
            for species, group in test_data.groupby('Species'):
                species_y_true = group['target']
                species_X = group.drop('target', axis=1)
                species_y_pred = self.predict(species_X)
                
                metrics[f'species_{species}'] = {
                    'accuracy': accuracy_score(species_y_true, species_y_pred),
                    'precision': precision_score(species_y_true, species_y_pred, average='weighted'),
                    'recall': recall_score(species_y_true, species_y_pred, average='weighted'),
                    'f1': f1_score(species_y_true, species_y_pred, average='weighted')
                }
        
        # Save confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        # Save feature importance if available
        if hasattr(self.best_model, 'feature_importances_'):
            metrics['feature_importance'] = {
                'features': X_test.columns.tolist(),
                'importance': self.best_model.feature_importances_.tolist()
            }
        
        # Save metrics
        with open(METRICS_PATH, 'w') as f:
            json.dump(metrics, f, indent=4)
            
        return metrics
    
    def save_model(self):
        """Save all models and encoders"""
        models = {
            'best_model': self.best_model,
            'species_models': self.species_specific_models,
            'label_encoder': self.label_encoder
        }
        joblib.dump(models, MODEL_PATH)
    
    def load_model(self):
        """Load all models and encoders"""
        models = joblib.load(MODEL_PATH)
        self.best_model = models['best_model']
        self.species_specific_models = models['species_models']
        self.label_encoder = models['label_encoder']