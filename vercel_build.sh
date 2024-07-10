#!/usr/bin/env bash
# Exit on error
set -o errexit
# create a virtual environment named 'venv' if it doesn't already exist
python3.11 -m venv venv

# activate the virtual environment
source venv/bin/activate
# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python3.11 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3.11 manage.py migrate