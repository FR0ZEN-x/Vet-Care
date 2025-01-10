#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Generate sample data if needed
python create_sample_data.py

# Train model if needed
python train_model.py

# Start the Flask server
python run.py 