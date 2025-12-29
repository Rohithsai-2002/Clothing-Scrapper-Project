@echo off
REM Batch script to run the clothing offers scraper
REM Place in Task Scheduler to run automatically

cd /d "c:\Users\rohit\OneDrive\Documents\Spam_Detection_Project"
call .venv\Scripts\activate.bat
python -m src.main
pause
