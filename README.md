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
- **Safety features** — safety timer, safe word alerts, risk assessment, escape plan generator
- **Document vault** — encrypted evidence storage with court-ready metadata
- **Peer support network** — anonymous chat with trained supporters
- **Legal rights bot** — Kenyan GBV law chatbot with legal references
- **Organization coordination** — resource inventory, AI case matching, inter-org messaging
- **Campaign manager** — multi-channel awareness campaigns (SMS, WhatsApp)
- **Virtual workshops** — live and recorded training sessions
- **Anonymous tips** — third-party reporting system
- **County scorecards** — performance tracking and rankings
- **Privacy policy** — user consent tracking (GDPR compliant)
- **Data export** — users can download their data (JSON/CSV)
- **SOS broadcast** — immediate multi-channel emergency response
- **Shelter booking** — direct emergency shelter reservations
- **Police report generation** — automated P3 form generation
- **Offline queue** — report submission without internet connection

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL / MySQL |
| Auth | SimpleJWT + django-allauth (Google OAuth) + django-otp (2FA) |
| File Storage | Cloudinary / Local (encrypted vault) |
| SMS | Africa's Talking SMS API |
| Payments | Paystack |
| Maps | Google Maps JavaScript API / Leaflet |
| AI | Groq API (LLaMA 3.3 70B) |
| Analytics | Pandas |
| API Docs | drf-spectacular + drf-yasg (Swagger UI, ReDoc) |
| Testing | pytest-django |
| Deployment | Render + Docker |

---


---

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL or MySQL
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/winstone-1/amakaziwatch.git
cd amakaziwatch
```
```
python3.12 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows Git Bash
```
```
pip install -r requirements.txt
```
```
cp .env.example .env
# Edit .env with your credentials
nano .env
```
```
sudo mysql
```
```
CREATE DATABASE amakaziwatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'amakaziwatch_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON amakaziwatch.* TO 'amakaziwatch_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
```
python manage.py migrate
```
```
python manage.py runserver
```
```
API root: http://127.0.0.1:8000/api
```
```
Swagger docs: http://127.0.0.1:8000/swagger/
```
```
ReDoc: http://127.0.0.1:8000/redoc/
```
```
Admin panel: http://127.0.0.1:8000/admin/
```
