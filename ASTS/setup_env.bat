:: Filename: setup_env.bat

@echo off
echo Setting up the virtual environment and installing dependencies...

:: Create the virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
pip install --upgrade pip

:: Install the required dependencies from requirements.txt
pip install -r requirements.txt

echo Environment setup complete.
pause
