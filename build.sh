#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput

# Remove problematic migration if exists
if [ -f "reports/migrations/0004_fix_report_models.py" ]; then
    rm reports/migrations/0004_fix_report_models.py
fi

# Run migrations
python manage.py migrate
