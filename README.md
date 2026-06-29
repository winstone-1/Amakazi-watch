# AmakaziWatch Backend API

> Kenya's first crowdsourced GBV awareness, reporting and prevention platform.

## Overview

AmakaziWatch is a Django REST Framework API that powers a comprehensive GBV (Gender-Based Violence) awareness and prevention platform for Kenya. It enables anonymous incident reporting, AI-powered classification, live heatmaps, organization coordination, and survivor safety tools.

## Tech Stack

* **Framework**: Django 6.0.5 + Django REST Framework 3.17.1
* **Database**: PostgreSQL (Render)
* **Auth**: JWT + Google OAuth + 2FA (TOTP)
* **File Storage**: Cloudinary
* **SMS**: Africa's Talking
* **Payments**: Paystack
* **AI**: Groq API (LLaMA)
* **Analytics**: Pandas
* **Deployment**: Render + Docker

## API Endpoints

| Category         | Endpoint                       | Method          | Auth      |
| ---------------- | ------------------------------ | --------------- | --------- |
| Auth             | `/api/auth/register/`          | POST            | None      |
| Auth             | `/api/auth/token/`             | POST            | None      |
| Auth             | `/api/auth/token/refresh/`     | POST            | None      |
| Auth             | `/api/auth/password-reset/`    | POST            | None      |
| Auth             | `/api/auth/password-change/`   | POST            | Bearer    |
| Auth             | `/api/auth/2fa/*`              | GET/POST        | Bearer    |
| Profile          | `/api/profile/`                | GET/PATCH       | Bearer    |
| Reports          | `/api/reports/`                | GET/POST        | Optional  |
| Reports          | `/api/reports/stats/`          | GET             | None      |
| Reports          | `/api/reports/heatmap/`        | GET             | Bearer    |
| Safety           | `/api/safety/timer/*`          | POST            | Bearer    |
| Safety           | `/api/safety/safe-word/*`      | POST            | Bearer    |
| Safety           | `/api/safety/risk-assessment/` | POST            | Bearer    |
| Safety           | `/api/safety/escape-plan/`     | POST            | Bearer    |
| Vault            | `/api/vault/documents/*`       | GET/POST/DELETE | Bearer    |
| Peer Support     | `/api/peer/sessions/*`         | GET/POST        | Bearer    |
| Legal Bot        | `/api/legal/ask/`              | POST            | None      |
| Organisations    | `/api/organisations/`          | GET/POST        | Optional  |
| Org Coordination | `/api/org/inventory/*`         | GET/POST        | Bearer    |
| Org Coordination | `/api/org/case-matching/`      | POST            | Bearer    |
| Content          | `/api/content/`                | GET             | None      |
| Campaigns        | `/api/campaigns/`              | GET/POST        | Bearer    |
| Workshops        | `/api/workshops/`              | GET/POST        | Bearer    |
| Tips             | `/api/tips/`                   | POST            | None      |
| Scorecards       | `/api/scorecard/rankings/`     | GET             | None      |
| Admin            | `/api/admin/*`                 | GET/POST        | Admin     |
| Terms            | `/api/terms/`                  | GET             | None      |
| Privacy          | `/api/privacy-policy/current/` | GET             | None      |
| Intelligence     | `/api/intelligence/*`          | GET             | X-API-Key |
| Chat             | `/api/chat/`                   | POST            | None      |
| Panic            | `/api/panic/`                  | POST            | Bearer    |
| Notifications    | `/api/notifications/`          | GET             | Bearer    |

## Installation

### Prerequisites

* Python 3.12+
* PostgreSQL
* Git

### Setup

```bash
git clone https://github.com/winstone-1/Amakazi-watch.git
cd Amakazi-watch

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

## Environment Variables

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/amakaziwatch

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Africa's Talking
AT_API_KEY=your-at-key
AT_USERNAME=sandbox
AT_SENDER_ID=AmakaziWatch

# Paystack
PAYSTACK_SECRET_KEY=your-paystack-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# Google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Groq
GROQ_API_KEY=your-groq-key
```

## Docker

```bash
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Testing

```bash
pytest
pytest --cov=.
```

## Deployment

### Render

* Push code to GitHub
* Create Web Service
* Build: `./build.sh`
* Start: `gunicorn amakaziwatch.wsgi:application`
* Add environment variables

### Docker

```bash
docker build -t amakazi-watch-api .
docker run -p 8000:8000 amakazi-watch-api
```

## Documentation

* Swagger: `/swagger/`
* ReDoc: `/redoc/`
* Schema: `/api/schema/`

## License

BSD License

**Author:** Winstone Mwangi
**GitHub:** @winstone-1
