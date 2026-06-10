FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Django settings module
ENV DJANGO_SETTINGS_MODULE=amakaziwatch.settings \
    SECRET_KEY=dummy-secret-key-for-build-only-do-not-use-in-production \
    DEBUG=False \
    DATABASE_URL=postgresql://amakaziwatch_user:woUgGiipbYVOYmQWCjQ2POZDoZrzOFWi@dpg-d8k6mumk1jcs739ka4gg-a.oregon-postgres.render.com/amakaziwatch

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Run collectstatic (will use the dummy settings above)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "amakaziwatch.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2", "--log-file", "-"]