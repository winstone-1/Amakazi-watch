# AmakaziWatch Backend API

> Kenya's first crowdsourced GBV awareness, reporting and prevention platform.
> Built with Django + Django REST Framework.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Author](#author)

---

## Overview

AmakaziWatch is a REST API backend that powers a GBV (Gender-Based Violence) awareness and prevention platform for Kenya. It enables:

- **Anonymous incident reporting** with SMS case reference via Africa's Talking
- **AI-powered report classification** using Groq LLM — urgency scoring and flagging
- **Live county heatmap** of anonymised reports for NGOs and county officials
- **Organisation directory** for NGOs, legal aid clinics and county government offices
- **Education hub** with articles, guides, YouTube videos and gamified quizzes
- **Paystack donations** directly to verified organisations
- **Pandas CSV analytics** — county summaries and trend reports for NGO donor reporting
- **Anonymous AI chatbot** for trauma-informed GBV support
- **JWT authentication** with role-based access control (RBAC)
- **Two-factor authentication** (TOTP) for admin and county official accounts
- **Password reset and change** endpoints

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL Deployed on render |
| Auth | SimpleJWT + django-allauth (Google OAuth) + django-otp (2FA) |
| File Storage | Cloudinary |
| SMS | Africa's Talking SMS API |
| Payments | Paystack |
| Maps | Google Maps JavaScript API |
| AI | Groq API (LLaMA 3.3 70B) |
| Analytics | Pandas |
| API Docs | drf-spectacular (Swagger UI at `/docs/`) |
| Testing | pytest-django |
| Deployment | Render + Docker |

---

## Project Structure

```
amakaziwatch/
├── amakaziwatch/          # Django config — settings, urls, wsgi
├── users/                 # Custom User model, RBAC roles, UserProfile
├── reports/               # IncidentReport model, anonymous submission, AI classifier
│   ├── management/
│   │   └── commands/
│   │       └── seed.py    # Database seeding command
│   └── utils/
│       ├── sms.py         # Africa's Talking SMS integration
│       ├── upload.py      # Cloudinary file upload utility
│       └── analytics.py   # Pandas CSV report generation
├── organisations/         # Organisation model, Donation, Paystack, Google Maps
│   └── utils/
│       ├── maps.py        # GeoJSON generation for Google Maps
│       └── paystack.py    # Paystack payment integration
├── content/               # EducationContent, Quiz, YouTube API
│   └── utils/
│       └── youtube.py     # YouTube Data API v3 search
├── api/                   # DRF serializers, views, urls
│   └── utils/
│       └── Groq.py        # Groq AI chatbot and report classifier
├── tests/
│   ├── test_models.py     # 5 model tests
│   └── test_api.py        # 15+ API endpoint tests
├── requirements.txt
├── pytest.ini
├── Procfile               # Render deployment
├── build.sh               # Render build script
└── .env.example           # Environment variables template
```

---

## Getting Started

### Prerequisites

- Python 3.12
- MySQL 8
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/winstone-1/amakaziwatch.git
cd amakaziwatch
```

**2. Create and activate virtual environment**
```bash
python3.12 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows Git Bash
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

**5. Create MySQL database**
```bash
sudo mysql
```
```sql
CREATE DATABASE amakaziwatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'amakaziwatch_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON amakaziwatch.* TO 'amakaziwatch_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Seed the database**
```bash
python manage.py seed
```

**8. Create superuser**
```bash
python manage.py createsuperuser
```

**9. Run the server**
```bash
python manage.py runserver
```

Visit:
- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

# MySQL
DB_NAME=amakaziwatch
DB_USER=amakaziwatch_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Cloudinary
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Africa's Talking
AT_API_KEY=
AT_USERNAME=sandbox
AT_SENDER_ID=AmakaziWatch

# Paystack
PAYSTACK_SECRET_KEY=sk_test_xxx
PAYSTACK_PUBLIC_KEY=pk_test_xxx

# Google
GOOGLE_MAPS_API_KEY=
YOUTUBE_API_KEY=

# Groq
GROQ_API_KEY=gsk_xxx

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

---

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

Full interactive docs available at `/docs/`

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register/` | None | Register new user |
| POST | `/auth/token/` | None | Login — returns JWT tokens |
| POST | `/auth/token/refresh/` | None | Refresh access token |
| POST | `/auth/password-reset/` | None | Request password reset email |
| POST | `/auth/password-reset/confirm/` | None | Confirm password reset |
| POST | `/auth/password-change/` | Required | Change password |
| GET | `/auth/2fa/setup/` | Required | Get 2FA QR code |
| POST | `/auth/2fa/setup/` | Required | Verify and enable 2FA |
| POST | `/auth/2fa/verify/` | Required | Verify 2FA code |
| POST | `/auth/2fa/disable/` | Required | Disable 2FA |

### Reports
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/reports/` | None | Submit anonymous report |
| GET | `/reports/heatmap/` | Required | County report counts |
| GET | `/reports/stats/` | None | Total stats + percentages by type |

### Organisations
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/organisations/` | None | List verified organisations |
| POST | `/organisations/register/` | None | Register new organisation |
| GET | `/organisations/map/` | None | GeoJSON for Google Maps |
| GET | `/organisations/heatmap/` | Required | Heatmap GeoJSON |
| GET | `/organisations/<id>/impact/` | Required | NGO impact dashboard stats |
| POST | `/organisations/<id>/bookmark/` | Required | Bookmark/unbookmark org |

### Content
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/content/` | None | List approved content |
| POST | `/content/create/` | Required | Submit content for approval |
| GET | `/content/featured/` | None | 3 latest articles + 1 quiz |
| GET | `/content/videos/` | None | YouTube video search |

### Quizzes
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/quizzes/` | None | List approved quizzes |
| POST | `/quizzes/<id>/complete/` | None | Record quiz completion |

### Donations
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/donations/initiate/` | None | Start Paystack donation |
| GET | `/donations/verify/` | None | Verify payment by reference |

### Analytics
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/analytics/county-summary/` | Required | Download county CSV report |
| GET | `/analytics/trend/` | Required | Download daily trend CSV |
| GET | `/analytics/county-official/` | County official | County-specific breakdown |

### Other
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/chat/` | None | AI chatbot (Groq LLaMA) |
| GET | `/search/?q=` | None | Search orgs, content, quizzes |
| GET | `/profile/` | Required | Get user profile |
| PATCH | `/profile/` | Required | Update user profile |

---

## User Roles

| Role | Access |
|---|---|
| `public` | Anonymous endpoints — report, chat, browse |
| `survivor` | Above + case history, bookmarks, profile |
| `org_staff` | Above + content submission, coverage heatmap |
| `county_official` | Above + county-specific heatmap and analytics |
| `admin` | Full access including Django admin panel |

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only model tests
pytest tests/test_models.py -v

# Run only API tests
pytest tests/test_api.py -v
```

Expected output: **20+ tests passing**

---

## Deployment

### Render (Production)

1. Push to GitHub
2. Connect repo on render.com
3. Set build command: `./build.sh`
4. Set start command: `gunicorn amakaziwatch.wsgi --log-file -`
5. Add all environment variables from `.env`
6. Set `DEBUG=False` and `ALLOWED_HOSTS=your-app.onrender.com`

### Docker

```bash
# Build image
docker build -t amakaziwatch .

# Run with docker-compose
docker-compose up
```

---

## Emergency Numbers

This platform always surfaces Kenya's GBV emergency contacts:

- **GBV Hotline:** 1195
- **Childline:** 116
- **Police:** 999

---

## Author

**Winstone Mwangi**
 · 2026
GitHub: [@winstone-1](https://github.com/winstone-1)

---

*AmakaziWatch — People Watch.*
