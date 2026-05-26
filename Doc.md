# AmakaziWatch 
### GBV Awareness, Community Reporting & Prevention Platform
**Django + DRF Capstone Project · 2026**
**Built by Winstone Mwangi**

---

## What is AmakaziWatch?

AmakaziWatch (*"People Watch"* in Swahili) is a community-powered platform that tackles Gender-Based Violence through three pillars: **anonymous incident reporting**, **public education**, and an **organisation directory** — all underpinned by a live county-level heatmap that turns community reports into actionable data for NGOs and county governments.

It is the first crowdsourced GBV early-warning system built specifically for Kenya.

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
- AI-powered anonymous chatbot for safe Q&A

### 3. Organisation Directory
NGOs, legal aid clinics, safe houses, and counselling centres register through Django admin-approved flow:
- Organisation profile: services, coverage area, contacts
- Verified badge system
- Google Maps integration — find organisations near you
- M-Pesa Daraja donate button — direct STK Push to listed NGOs

---

## UI — Pages & What They Contain

### Home `/`
- Bold hero with two CTAs: *Report Anonymously* and *Find Help Near Me*
- Crisis banner: Africa's Talking SMS number for non-smartphone users
- Live counters: reports this month, organisations listed
- Three feature cards explaining the pillars
- Latest 3 education articles
- Footer: emergency numbers — GBV Hotline 1195, Childline 116

### Report Page `/report`
- Multi-step form — no account required
  - Step 1: abuse type icon grid
  - Step 2: county/sub-county dropdowns
  - Step 3: description + optional Cloudinary image upload
  - Step 4: optional phone number for SMS case reference
- Progress bar across steps
- Plain-language copy at every step to reduce fear and friction
- Confirmation screen with case reference + SMS sent via Africa's Talking

### Education Hub `/learn`
- Filter bar: by topic and format (article, video, guide)
- Article cards with organisation author, read time, topic badge
- YouTube video embeds via YouTube Data API
- AI chat widget (bottom-right): anonymous Q&A powered by Anthropic Claude API
- PDF resource download cards for community health workers

### Organisation Directory `/organisations`
- Search bar + county filter
- Card grid: name, services, coverage area, verified badge
- Google Maps panel with clustered org pins
- Org detail page: full profile + M-Pesa donate button

### Heatmap Dashboard `/heatmap` — NGO & Admin only
- Choropleth map of Kenya: counties coloured by report density
- Filter by abuse type, date range, sub-county
- Trend line chart: reports over time
- CSV export for NGO reporting
- RBAC-protected: only verified org staff and admin

### Organisation Registration `/register/org`
- Multi-step: org details, services, coverage area, document upload (Cloudinary)
- Pending state until admin approves
- On approval: account gets `org_staff` role

### Auth Pages `/login` `/register` `/password-reset`
- Django built-in auth + crispy forms styling
- Google Sign-In via django-allauth for org accounts
- Two-factor auth for admin accounts

### Django Admin `/admin`
- Approve/reject organisation registrations
- Moderate education content
- View all anonymised reports with filters
- Manage user roles

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Auth | Django built-in + SimpleJWT + django-allauth (Google OAuth) |
| Database | SQLite (dev) → PostgreSQL (Render prod) |
| File Storage | Cloudinary — evidence photos, org docs, PDF guides |
| SMS | Africa's Talking SMS API — case reference delivery |
| Maps | Google Maps JavaScript API — org directory + heatmap |
| Payments | M-Pesa Daraja STK Push — NGO donations |
| Video | YouTube Data API v3 — education hub |
| AI | Anthropic Claude API — chatbot + report classifier + content moderation |
| Frontend (now) | Django Templates + Bootstrap 5 + Vanilla JS |
| Frontend (later) | React 19 + Vite + Tailwind v4 → connects to DRF API |
| Deployment | Render |
| Testing | pytest-django |
| API Docs | drf-spectacular (Swagger) |

---

## AI Integration

### Anonymous Support Chatbot
Floating chat widget on `/learn`. Powered by Anthropic Claude API. Users ask questions like *"Is what my partner doing abuse?"* and get safe, trauma-informed responses. No account needed, nothing persisted server-side. Always surfaces the national hotline (1195) for crisis situations.

### Report Urgency Classifier
On report submission, a background task sends the description to Claude which returns:
- Abuse type cross-check
- Urgency score 1–5 based on language cues
- Flag if children or immediate danger are mentioned

Visible only to admin. Helps triage at scale.

### Content Moderation Assistant
When an org submits an education article, Claude reviews it and flags victim-blaming language, suggests plain-language improvements, and gives admin a pre-review summary. Speeds up the approval workflow significantly.

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
| GET | `/api/content/` | List approved education content |
| POST | `/api/content/` | Submit content (org staff only) |
| POST | `/api/donations/initiate/` | Trigger M-Pesa STK Push |
| POST | `/api/donations/callback/` | Safaricom Daraja webhook |
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
| Grant funding | iHub, Antler Kenya, Chandaria social impact tracks — apply with the working capstone as proof |

### Long-term
| Stream | Model |
|---|---|
| API access | Charge NGOs to query the heatmap data programmatically for their own dashboards |
| Mobile app (React Native/Expo) | Free for survivors, premium features for org staff |

**Positioning:** AmakaziWatch is infrastructure, not just an app. The county heatmap is the moat — no one else is building this for Kenya. That's the story for investors and institutional buyers.

---
## 3-Day Execution Plan

### Day 1 — Tuesday 27 May · Setup + Models + Auth
- [ ] settings.py fully configured (all packages, Cloudinary, JWT, CORS)
- [ ] Custom User model with RBAC roles
- [ ] All 5 models defined and migrated
- [ ] Django admin registered with list_display and actions
- [ ] Superuser created, admin panel verified
- [ ] Built-in auth: login, register, logout, password reset
- [ ] Seed data: 3 orgs, 5 reports, 3 content items
- [ ] First pytest tests passing

### Day 2 — Wednesday 28 May · DRF API + Integrations
- [ ] All serializers and ViewSets built
- [ ] JWT auth endpoints working (Postman tested)
- [ ] Google OAuth via django-allauth
- [ ] Africa's Talking SMS on report submit
- [ ] M-Pesa Daraja STK Push + callback endpoint
- [ ] Google Maps org directory
- [ ] YouTube API education hub
- [ ] Claude API chatbot + report classifier
- [ ] Swagger docs at `/docs/`
- [ ] API rate limiting and security
- [ ] Django templates: all pages rendering

### Day 3 — Thursday 29 May · Polish + Deploy + Present
- [ ] Bootstrap 5 CSS polish, mobile responsive
- [ ] pytest suite: 10+ tests passing
- [ ] Deploy to Render with all env vars set
- [ ] End-to-end test on live URL
- [ ] 3-minute demo script prepared

---

