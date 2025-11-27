#!/usr/bin/env bash

echo "🚀 Starting build and run script..."

echo "📌 Activating virtual environment..."
source ~/.virtualenvs/Volunteer-Event-Coordination-ZZnVOrS2/Scripts/activate

echo "📦 Installing dependencies..."
pip install pytest coverage mysql-connector-python

echo "🗄️ Initializing database..."

# PATH to MAMP MySQL on Windows
MYSQL_PATH="/c/MAMP/bin/mysql/bin/mysql.exe"

if [ ! -f "$MYSQL_PATH" ]; then
  echo "❌ ERROR: MySQL not found at $MYSQL_PATH"
  exit 1
fi

# Run SQL (YOUR REAL FILES)
"$MYSQL_PATH" -u root -proot < "./database/scripts/reset_db.sql"
"$MYSQL_PATH" -u root -proot < "./database/scripts/schema_seed.sql"

echo "Database initialized successfully!"

echo "▶️ Running the application..."

# Make Python see the src folder
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"

python ./src/volunteer_event_coordination/main.py -c ./config/app_config.json

