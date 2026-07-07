#!/bin/sh
set -e

echo "⏳ Waiting for PostgreSQL..."
until nc -z db 5432; do
  echo "PostgreSQL not ready yet, waiting..."
  sleep 2
done
echo "✅ PostgreSQL ready!"

echo "🔄 Applying migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:8000
