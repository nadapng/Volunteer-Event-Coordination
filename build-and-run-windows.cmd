@echo off
echo 🚀 Starting Windows build-and-run...

REM ============ 1) Activate virtual environment ============
echo 📌 Activating virtual environment...
call %USERPROFILE%\.virtualenvs\Volunteer-Event-Coordination-ZZnVOrS2\Scripts\activate

REM ============ 2) Run tests + coverage ============
echo 🧪 Running tests...
coverage run -m pytest
coverage report -m

REM ============ 3) Run the application ============
echo ▶️ Running the application...

cd src
python -m volunteer_event_coordination.main -c ../config/application_name_app_config.json
cd ..
