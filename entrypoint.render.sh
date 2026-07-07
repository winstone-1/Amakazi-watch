#!/bin/sh
set -e

echo "🚀 Starting AmakaziWatch on Render..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL is not set!"
    echo "Please add DATABASE_URL to your Render environment variables."
    exit 1
fi

echo "✅ DATABASE_URL is set"

# Wait for database to be ready (simple retry)
echo "⏳ Checking database connection..."
MAX_RETRIES=30
RETRY_COUNT=0

until python -c "import psycopg2, os; psycopg2.connect(os.environ['DATABASE_URL'])" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "❌ Database not ready after $MAX_RETRIES attempts"
        exit 1
    fi
    echo "⏳ Waiting for database... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

echo "✅ Database is ready!"

# Run migrations
echo "🔄 Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (optional)
echo "👤 Ensuring superuser exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" 2>/dev/null || true

echo "🚀 Starting Gunicorn..."
exec gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:$PORT
