import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
DATASET_PATH = os.path.join(BASE_DIR, 'data', 'veterinary_data.csv')
METRICS_PATH = os.path.join(BASE_DIR, 'models', 'metrics.json')

# Model configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Feature lists
CATEGORICAL_FEATURES = ['Species', 'Gender', 'Diet_Type', 'Habitat_Quality', 'Genetic_Risk', 'Medical_History']
NUMERICAL_FEATURES = ['Age', 'Weight', 'Heart_Rate', 'Respiratory_Rate', 'Temperature']

# Create required directories if they don't exist
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)

# Flask application settings
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Model settings
MODEL_PATH = 'models/health_analysis_model.pkl'
SCALER_PATH = 'models/scaler.pkl'
LABEL_ENCODERS_PATH = 'models/label_encoders.pkl'

# Species-specific vital signs ranges
SPECIES_RANGES = {
    'Dog': {
        'heart_rate': (60, 140),
        'respiratory_rate': (10, 30),
        'temperature': (37.5, 39.2)
    },
    'Cat': {
        'heart_rate': (120, 140),
        'respiratory_rate': (20, 30),
        'temperature': (38.0, 39.2)
    },
    'Horse': {
        'heart_rate': (28, 44),
        'respiratory_rate': (8, 16),
        'temperature': (37.5, 38.5)
    },
    'Bird': {
        'heart_rate': (200, 400),
        'respiratory_rate': (25, 45),
        'temperature': (39.5, 42.5)
    },
    'Reptile': {
        'heart_rate': (60, 100),
        'respiratory_rate': (10, 30),
        'temperature': (35.0, 37.8)
    }
}

# Symptom severity mapping
SYMPTOM_SEVERITY = {
    'Lethargy': 3,
    'Loss of Appetite': 2,
    'Weight Loss': 3,
    'Fever': 2,
    'Dehydration': 3,
    'Coughing': 2,
    'Sneezing': 1,
    'Difficulty Breathing': 4,
    'Nasal Discharge': 2,
    'Vomiting': 3,
    'Diarrhea': 3
}