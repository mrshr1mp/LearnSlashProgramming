@echo off
cd /d "%~dp0"
rem pythonw runs the app without a console window; the app quits on its own after you close its window
where pythonw >nul 2>nul && (start "" pythonw app.py) || (python app.py)
