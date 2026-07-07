#!/bin/sh
set -e

echo "🚀 Starting AmakaziWatch on Render..."

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL is not set!"
    exit 1
fi

echo "✅ DATABASE_URL is set"

echo "⏳ Checking database connection..."
python -c "import psycopg2, os; psycopg2.connect(os.environ['DATABASE_URL'])" 2>/dev/null || {
    echo "❌ Database connection failed!"
    exit 1
}

echo "✅ Database is ready!"

echo "🔄 Applying migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
PORT=${PORT:-10000}
exec gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:$PORT --workers=1 --threads=2 --timeout=30
