#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Navigate to the frontend directory
cd frontend

# Install npm dependencies
npm install

# Build the React app
npm run build

# Navigate back to the root directory
cd ..

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Start the Gunicorn server
gunicorn school_manage.wsgi:application