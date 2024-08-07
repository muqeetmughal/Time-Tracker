#!/usr/bin/env bash
# Exit on error
set -o errexit
./env/bin/python manage.py migrate
./env/bin/python manage.py runserver 0.0.0.0:8000