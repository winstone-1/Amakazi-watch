#!/bin/sh
# Wait for PostgreSQL to be ready

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:8000
