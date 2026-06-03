# AmakaziWatch 
### GBV Awareness, Community Reporting & Prevention Platform
**Django + DRF Backend Capstone ·  · 2026**
**Built by Winstone Mwangi**

---

## What is AmakaziWatch?

AmakaziWatch (*"People Watch"* in Swahili) is a community-powered platform that tackles Gender-Based Violence through three pillars: **anonymous incident reporting**, **public education**, and an **organisation directory** — all underpinned by a live county-level heatmap that turns community reports into actionable data for NGOs and county governments.

It is the first crowdsourced GBV early-warning system built specifically for Kenya.

> **Presentation timeline:**
> - **Monday 2 June 2026** — Backend capstone presentation (Django + DRF)
> - **Phase 2 (post-capstone)** — React 19 + Vite + Tailwind v4 frontend
> - **Thursday 29 May** — Deployment & Docker  

---

## The Problem

GBV in Kenya kills, maims, and silences thousands every year. The barriers to action are not just cultural — they are **informational and structural**:

- Most people cannot recognise early abuse signs (financial control, isolation, emotional manipulation) until physical harm has occurred
- Survivors and bystanders don't know who to call or where to go
- County governments and NGOs have no live data on where GBV is concentrated — they rely on surveys done every 3–5 years
- Education materials exist but are inaccessible to people on basic phones or slow connections
- NGOs operate in silos with no shared directory or referral network

AmakaziWatch closes all five gaps.

---

## The Three Pillars

### 1. Anonymous Incident Reporting
Any person — survivor, witness, or community member — can file a report with **zero account creation**. The form captures:
- Type of abuse (physical, emotional, financial, sexual, digital)
- Relationship to victim (self, family, neighbour, colleague)
- County and sub-county (not full address — privacy first)
- Optional: upload evidence photo via Cloudinary
- Optional: receive SMS case reference via Africa's Talking

Reports feed a live heatmap visible to verified NGOs and admin. No names are ever stored.

### 2. Education & Awareness Hub
A library of verified content published by registered organisations and approved by admin:
- Articles on recognising abuse and legal rights under Kenyan law (Protection Against Domestic Violence Act, 2015)
- Video content via YouTube Data API
- Downloadable PDF guides for community health workers (Cloudinary)
- Gamified awareness quizzes with anonymised completion tracking
- AI-powered anonymous chatbot for safe Q&A

### 3. Organisation Directory
NGOs, legal aid clinics, safe houses, and counselling centres register through Django admin-approved flow:
- Organisation profile: services, coverage area, contacts
- Verified badge system
- Google Maps integration — find organisations near you
- M-Pesa Daraja donate button — direct STK Push to listed NGOs
- NGO impact dashboard: reports responded to, donations received, referrals made

---


## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Auth | Django built-in + SimpleJWT + django-allauth (Google OAuth) |
| Database | MySQL (dev + prod) |
| File Storage | Cloudinary — evidence photos, org docs, PDF guides |
| SMS | Africa's Talking SMS API — case reference delivery |
| Maps | Google Maps JavaScript API — org directory + heatmap |
| Payments | M-Pesa Daraja STK Push — NGO donations |
| Video | YouTube Data API v3 — education hub |
| AI | Anthropic Claude API — chatbot + report classifier + content moderation |
| Frontend (Phase 1) | Django Templates + Bootstrap 5 + Vanilla JS |
| Frontend (Phase 2) | React 19 + Vite + Tailwind v4 → connects to DRF API |
| Deployment | Render + Docker |
| Testing | pytest-django |
| API Docs | drf-spectacular (Swagger) |

---

## AI Integration

### Anonymous Support Chatbot
Floating chat widget on `/learn`. Powered by Anthropic Groq API. Users ask questions like *"Is what my partner doing abuse?"* and get safe, trauma-informed responses. No account needed, nothing persisted server-side. Always surfaces the national hotline (1195) for crisis situations.

### Report Urgency Classifier
On report submission, a background task sends the description to Claude which returns:
- Abuse type cross-check
- Urgency score 1–5 based on language cues
- Flag if children or immediate danger are mentioned

Visible only to admin. Helps triage at scale.

### Content Moderation Assistant
When an org submits an education article, Claude reviews it and flags victim-blaming language, suggests plain-language improvements, and gives admin a pre-review summary. Speeds up the approval workflow.

---

## Data Models

```
User (custom AbstractUser)
  └── role: admin / org_staff / public
  └── organisation FK (nullable)

Organisation
  └── name, description, services, county, sub_county
  └── latitude, longitude, verified, document_url (Cloudinary)

IncidentReport  [NO user FK — anonymous]
  └── abuse_type, relationship, county, sub_county, description
  └── evidence_url (Cloudinary), sms_ref_code
  └── urgency_score (AI), ai_classification, flagged_for_review

EducationContent
  └── title, body, format, topic, organisation FK
  └── youtube_url, pdf_url (Cloudinary), approved, ai_review_notes

Quiz
  └── title, topic, organisation FK, approved
  └── questions (JSON field): [{question, options[], correct_index}]
  └── completion_count (anonymised)

Donation
  └── organisation FK, amount, phone
  └── mpesa_checkout_id, mpesa_receipt, status

SMSLog
  └── phone_hash (hashed — never raw), ref_code, sent_at, status
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/reports/` | Submit anonymous report |
| GET | `/api/reports/heatmap/` | County aggregates — NGO/admin only |
| GET | `/api/organisations/` | List verified organisations |
| POST | `/api/organisations/register/` | Register new organisation |
| GET | `/api/organisations/<id>/impact/` | NGO impact stats |
| GET | `/api/content/` | List approved education content |
| POST | `/api/content/` | Submit content (org staff only) |
| GET | `/api/quizzes/` | List approved quizzes |
| POST | `/api/quizzes/<id>/complete/` | Log anonymised quiz completion |
| POST | `/api/donations/initiate/` | Trigger M-Pesa STK Push |
| POST | `/api/donations/callback/` | Paystack webhook |
| POST | `/api/chat/` | Anonymous AI chatbot |
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/token/` | JWT login |
| POST | `/api/auth/token/refresh/` | Refresh token |
| GET | `/api/auth/google/` | Google OAuth |
| GET | `/docs/` | Swagger UI |

---

## Monetization Strategy

### Immediate (post-capstone)
| Stream | Model | Estimated Revenue |
|---|---|---|
| NGO heatmap subscriptions | KES 5,000–15,000/month per org | Recurring SaaS |
| Verified listing badge | KES 2,000–5,000 one-time | Scales with directory growth |
| Onboarding & training workshops | KES 20,000–50,000 per org | Services |

### Medium-term
| Stream | Model |
|---|---|
| White-label licensing | County governments and UN agencies pay to run their own branded instance |
| Research data partnerships | Anonymised aggregate trend data licensed to academic institutions and policy orgs (SVRI, UN Women) |
| Corporate CSR partnerships | Companies sponsor SMS awareness blasts or fund education content |
| Grant funding | iHub, Antler Kenya, Chandaria social impact tracks — apply with working capstone as proof |

### Long-term
| Stream | Model |
|---|---|
| API access | Charge NGOs to query heatmap data programmatically for their own dashboards |
| Mobile app (React Native/Expo) | Free for survivors, premium features for org staff |
| Safaricom Bonga Points integration | Donors contribute loyalty points to NGOs via M-Pesa Daraja |

**Positioning:** AmakaziWatch is infrastructure, not just an app. The county heatmap is the moat — no one else is building this for Kenya.

---

## Full Roadmap

### Phase 1 — Backend Capstone 
- Django + DRF API, MySQL, JWT auth, Google OAuth
- Anonymous reporting + Africa's Talking SMS
- Cloudinary file storage
- M-Pesa Daraja donations
- Google Maps org directory
- Groq AI chatbot + report classifier + content moderation
- Gamified quizzes + NGO impact dashboard
- Swagger docs + pytest suite
- Deployed on Render

### Phase 2 — React Frontend (2–4 weeks post-capstone)
- React 19 + Vite + Tailwind v4 (same stack as Perfect Pick)
- Deploy on Vercel
- JWT auth in httpOnly cookies + Google OAuth
- Mapbox GL JS for richer heatmap
- All Django template pages rebuilt as React routes

### Phase 3 — Growth Features (1–3 months)
- **WhatsApp Bot** — Africa's Talking WhatsApp API for reporting, directory search, and education delivery
- **Predictive heatmap alerts** — auto SMS/email to NGOs when reports spike in their county
- **Survivor stories** — anonymous moderated section with AI safety review
- **Monthly PDF reports** — auto-generated with Django + Celery for NGO donor reporting
- **Multi-language support** — Django i18n: Swahili, Sheng, Kikuyu, Somali
- **Referral network** — NGOs refer cases to each other, backend tracks referral chains

### Phase 4 — Infrastructure & Scale
- **Offline-first PWA** — service workers + IndexedDB, auto-sync on reconnect
- **Voice reporting** — Africa's Talking voice API, AI transcription + classification
- **Secure evidence vault** — encrypted uploads, Django + AWS KMS, legal-aid-only access
- **AI pattern detection** — clustering models to detect hidden abuse epidemics by county
- **React Native app** — Expo + EAS Build, push notifications for awareness campaigns
- **Docker + CI/CD** — containerised deployment, GitHub Actions pipeline

---

## Execution Plan (Tuesday 27 May → Monday 2 June)

### Today — Tuesday 27 May · Settings + Models + Auth
- [ ] `settings.py` fully configured (MySQL, Cloudinary, JWT, CORS, allauth)
- [ ] Custom User model with RBAC roles
- [ ] All models migrated (User, Organisation, IncidentReport, EducationContent, Quiz, Donation, SMSLog)
- [ ] Django admin registered with list_display and actions
- [ ] Superuser created, admin panel verified
- [ ] Built-in auth: login, register, logout, password reset
- [ ] `git commit -m "feat(models): define all models and configure settings"`

### Wednesday 28 May · DRF API + JWT + Cloudinary
- [ ] All serializers and ViewSets built
- [ ] JWT auth endpoints (Postman tested)
- [ ] Google OAuth via django-allauth
- [ ] Cloudinary file upload working (evidence photos, org docs)
- [ ] Swagger docs at `/docs/`
- [ ] `git commit -m "feat(api): DRF serializers, ViewSets, JWT auth, Swagger"`

### Thursday 29 May · Integrations (class day — work after)
- [ ] Africa's Talking SMS on report submit
- [ ] M-Pesa Daraja STK Push + callback
- [ ] Google Maps org directory endpoint
- [ ] YouTube API education hub
- [ ] `git commit -m "feat(integrations): AT SMS, M-Pesa Daraja, Google Maps, YouTube API"`

### Friday 30 May · AI + Templates + Tests
- [ ] Groq API chatbot endpoint
- [ ] Report urgency classifier
- [ ] Content moderation assistant
- [ ] Django templates: all pages rendering cleanly
- [ ] Quiz model + completion tracking
- [ ] NGO impact dashboard
- [ ] pytest suite: 15+ tests passing
- [ ] `git commit -m "feat(ai): Claude chatbot, classifier, moderation + templates + tests"`

### Saturday 31 May · Polish + Security
- [ ] API rate limiting on anonymous endpoints
- [ ] RBAC double-checked on all protected routes
- [ ] Bootstrap 5 CSS polish, mobile responsive
- [ ] Seed data: 5 orgs, 10 reports, 5 content items, 3 quizzes
- [ ] `git commit -m "feat(security): rate limiting, RBAC hardening, seed data"`

### Sunday 1 June · Deploy + Rehearse
- [ ] Deploy to Render with all env vars configured
- [ ] End-to-end test on live URL
- [ ] Docker container (learned Thursday — apply it)
- [ ] 3-minute demo script practiced
- [ ] `git commit -m "chore(deploy): Render deployment, Docker config"`

### Monday 2 June · Present 🎯

---

## Presentation Talking Points

1. **The data gap** — Kenya has GBV stats from surveys every 3–5 years. AmakaziWatch generates live county-level data
2. **The reach** — SMS reporting means a person with a basic phone in Kisumu can report without a smartphone
3. **The AI layer** — classifier helps admin triage hundreds of reports, chatbot gives survivors a safe first contact
4. **The architecture** — Django templates now, React later. DRF API is already the contract for the frontend
5. **The quizzes** — gamified awareness is not just UX sugar, it generates anonymised engagement data NGOs can use
6. **The business** — NGO subscriptions, verified listings, white-label licensing, accelerator funding

---

## Folder Structure

```
amakaziwatch/
├── manage.py
├── requirements.txt
├── pytest.ini
├── .env
├── .env.example
├── .gitignore
├── amakaziwatch/        ← Django config (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               ← Custom User model, RBAC roles
├── reports/             ← IncidentReport, anonymous form, AI classifier
├── organisations/       ← Organisation model, M-Pesa donations, impact dashboard
├── content/             ← EducationContent, Quiz, YouTube API, AI moderation
├── api/                 ← DRF serializers, ViewSets, JWT, Swagger
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── report.html
│   ├── learn.html
│   ├── organisations.html
│   ├── heatmap.html
│   └── dashboard.html
├── static/
│   ├── css/
│   └── js/
└── tests/
    ├── test_models.py
    ├── test_views.py
    ├── test_forms.py
    └── test_api.py
```

---

*AmakaziWatch — People Watch. Built by Winstone Mwangi ·  2026*
