#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput || true