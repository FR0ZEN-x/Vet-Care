# VetCare - Veterinary Health Analysis System

## Overview
VetCare is an intelligent veterinary health analysis system designed to help veterinarians and pet owners monitor and assess animal health conditions. The system provides real-time health analysis, disease risk assessment, and care recommendations for various animal species.

## Features
- Multi-species health analysis
- Real-time vital signs monitoring
- Disease risk assessment
- Customized care recommendations
- Environmental factor analysis
- Species-specific metrics evaluation

## Technical Requirements
- Python 3.8+
- Flask web framework
- Scientific computing libraries (NumPy, Pandas)
- Machine Learning capabilities (scikit-learn)

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/vetcare.git
cd vetcare

2. Create a virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

## Project Structure

vetcare/
├── app.py              # Main Flask application
├── species_config.py   # Species configuration and parameters
├── species_metrics.py  # Metrics analysis implementation
├── disease_analysis.py # Disease risk assessment
├── templates/         # HTML templates
│   ├── index.html
│   └── landing.html
├── static/           # Static files (CSS, JS, images)
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation

## API Endpoints

### GET /api/species-info
Returns information about supported species and categories.

### POST /predict
Performs health analysis based on provided metrics.

Request body example:
```json
{
    "Species": "Dog",
    "Age": 5,
    "Weight": 25,
    "Temperature": 38.5,
    "HeartRate": 90,
    "RespiratoryRate": 20
}
```

## Running the Application

Development mode:
set FLASK_APP=app.py
set FLASK_DEBUG=1
python app.py or flask run or python -m flask run (If using a virtual environment)

Production mode:
gunicorn app:app

## Testing
Run the test suite:
pytest
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Author

Shaik Abdul Munawar

[LinkedIn Profile](https://www.linkedin.com/in/shaik-abdul-munawar-b35821284)
