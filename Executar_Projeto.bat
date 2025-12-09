@ECHO OFF

:: Install required python modules:
pip install -r requirements.txt

:: Runs project:
Python.exe "./src/script.py"