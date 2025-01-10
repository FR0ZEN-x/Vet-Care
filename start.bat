@echo off
echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Generating sample data...
python create_sample_data.py

echo.
echo Training model...
python train_model.py

echo.
echo Starting Flask server...
python run.py 