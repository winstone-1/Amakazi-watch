#!/bin/sh
set -e
echo "🚀 Starting..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:$PORT --workers=1 --threads=2 --timeout=30
