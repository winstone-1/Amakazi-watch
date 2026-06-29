#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Make migrations before running migrate
python manage.py makemigrations --noinput

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput