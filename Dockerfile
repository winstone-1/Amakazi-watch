FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE=amakaziwatch.settings \
    SECRET_KEY=dummy-secret-key-for-build-only-do-not-use-in-production \
    DEBUG=False

ENV DATABASE_URL=postgresql://amakaziwatch_user:woUgGiipbYVOYmQWCjQ2POZDoZrzOFWi@dpg-d8k6mumk1jcs739ka4gg-a.oregon-postgres.render.com/amakaziwatch

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p staticfiles

# Debug collectstatic - show what's happening
RUN echo "=== Checking Django installation ===" && \
    python -c "import django; print(f'Django version: {django.get_version()}')" && \
    echo "=== Running collectstatic ===" && \
    python manage.py collectstatic --noinput --verbosity 2 || \
    echo "=== Collectstatic failed but continuing ==="

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn amakaziwatch.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-file -"]