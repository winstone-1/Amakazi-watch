import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from reports.models import IncidentReport
from organisations.models import Organisation
from content.models import EducationContent, Quiz

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@amakaziwatch.com",
        password="Test@1234"
    )


@pytest.fixture
def auth_client(client, user):
    response = client.post("/api/auth/token/", {
        "username": "testuser",
        "password": "Test@1234"
    }, format="json")
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def org(db):
    return Organisation.objects.create(
        name="Test NGO",
        description="Test",
        services="counselling",
        county="Nairobi",
        verified=True,
    )


# ── Auth Tests ────────────────────────────────────────────────────────────────
@pytest.mark.django_db
def test_register_user(client):
    response = client.post("/api/auth/register/", {
        "username": "newuser",
        "email": "new@test.com",
        "password": "Test@1234"
    }, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "newuser"


@pytest.mark.django_db
def test_login_returns_token(client, user):
    response = client.post("/api/auth/token/", {
        "username": "testuser",
        "password": "Test@1234"
    }, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password(client, user):
    response = client.post("/api/auth/token/", {
        "username": "testuser",
        "password": "wrongpassword"
    }, format="json")
    assert response.status_code == 401


# ── Report Tests ──────────────────────────────────────────────────────────────
@pytest.mark.django_db
def test_submit_report_no_auth(client):
    response = client.post("/api/reports/", {
        "abuse_type": "physical",
        "relationship": "self",
        "county": "Nairobi",
        "sub_county": "Westlands",
        "description": "Test report"
    }, format="json")
    assert response.status_code == 201
    assert "ref_code" in response.data


@pytest.mark.django_db
def test_report_generates_ref_code(client):
    response = client.post("/api/reports/", {
        "abuse_type": "emotional",
        "relationship": "family",
        "county": "Mombasa",
    }, format="json")
    assert response.status_code == 201
    assert len(response.data["ref_code"]) == 8


@pytest.mark.django_db
def test_heatmap_requires_auth(client):
    response = client.get("/api/reports/heatmap/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_heatmap_with_auth(auth_client):
    response = auth_client.get("/api/reports/heatmap/")
    assert response.status_code == 200


# ── Organisation Tests ────────────────────────────────────────────────────────
@pytest.mark.django_db
def test_list_organisations_public(client, org):
    response = client.get("/api/organisations/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_unverified_org_not_listed(client):
    Organisation.objects.create(
        name="Unverified NGO",
        description="Test",
        services="legal aid",
        county="Kisumu",
        verified=False,
    )
    response = client.get("/api/organisations/")
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_filter_organisations_by_county(client, org):
    Organisation.objects.create(
        name="Mombasa NGO",
        description="Test",
        services="counselling",
        county="Mombasa",
        verified=True,
    )
    response = client.get("/api/organisations/?county=Nairobi")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["county"] == "Nairobi"


# ── Content Tests ─────────────────────────────────────────────────────────────
@pytest.mark.django_db
def test_list_content_public(client, org):
    EducationContent.objects.create(
        title="Test Article",
        body="Test body",
        format="article",
        topic="legal",
        organisation=org,
        approved=True,
    )
    response = client.get("/api/content/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_unapproved_content_not_listed(client, org):
    EducationContent.objects.create(
        title="Unapproved Article",
        body="Test",
        format="article",
        topic="legal",
        organisation=org,
        approved=False,
    )
    response = client.get("/api/content/")
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_content_requires_auth(client, org):
    response = client.post("/api/content/create/", {
        "title": "Test",
        "body": "Test body",
        "format": "article",
        "topic": "legal",
        "organisation": org.id,
    }, format="json")
    assert response.status_code == 401


# ── Analytics Tests ───────────────────────────────────────────────────────────
@pytest.mark.django_db
def test_analytics_requires_auth(client):
    response = client.get("/api/analytics/county-summary/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_analytics_with_auth_no_data(auth_client):
    response = auth_client.get("/api/analytics/county-summary/")
    assert response.status_code == 404


# -- Password Reset Tests -----------------------------------------------------
@pytest.mark.django_db
def test_password_reset_request_valid_email(client, user):
    response = client.post("/api/auth/password-reset/", {
        "email": "test@amakaziwatch.com"
    }, format="json")
    assert response.status_code == 200
    assert "message" in response.data


@pytest.mark.django_db
def test_password_reset_request_invalid_email(client):
    response = client.post("/api/auth/password-reset/", {
        "email": "nonexistent@test.com"
    }, format="json")
    # Always returns 200 to prevent email enumeration
    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset_missing_email(client):
    response = client.post("/api/auth/password-reset/", {}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_password_change_correct(auth_client):
    response = auth_client.post("/api/auth/password-change/", {
        "old_password": "Test@1234",
        "new_password": "NewPass@5678"
    }, format="json")
    assert response.status_code == 200
    assert "message" in response.data


@pytest.mark.django_db
def test_password_change_wrong_old_password(auth_client):
    response = auth_client.post("/api/auth/password-change/", {
        "old_password": "wrongpassword",
        "new_password": "NewPass@5678"
    }, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_password_change_requires_auth(client):
    response = client.post("/api/auth/password-change/", {
        "old_password": "Test@1234",
        "new_password": "NewPass@5678"
    }, format="json")
    assert response.status_code == 401


# -- 2FA Tests ----------------------------------------------------------------
@pytest.mark.django_db
def test_2fa_setup_returns_qr(auth_client):
    response = auth_client.get("/api/auth/2fa/setup/")
    assert response.status_code == 200
    assert "qr_code" in response.data
    assert "secret" in response.data


@pytest.mark.django_db
def test_2fa_verify_invalid_code(auth_client):
    # Setup first
    auth_client.get("/api/auth/2fa/setup/")
    response = auth_client.post("/api/auth/2fa/verify/", {
        "code": "000000"
    }, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_2fa_disable_requires_password(auth_client):
    response = auth_client.post("/api/auth/2fa/disable/", {}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_2fa_disable_wrong_password(auth_client):
    response = auth_client.post("/api/auth/2fa/disable/", {
        "password": "wrongpassword"
    }, format="json")
    assert response.status_code == 400


def test_safety_timer_start(auth_client):
    response = auth_client.post('/api/safety/timer/start/', {
        'duration_minutes': 30
    })
    assert response.status_code == 201

def test_safe_word_create(auth_client):
    response = auth_client.post('/api/safety/safe-word/', {
        'code_word': 'blueberry'
    })
    assert response.status_code == 201

def test_risk_assessment(auth_client):
    response = auth_client.post('/api/safety/risk-assessment/', {
        'answers': {'q1': True, 'q2': False}
    })
    assert response.status_code == 201

def test_escape_plan(auth_client):
    response = auth_client.post('/api/safety/escape-plan/', {
        'county': 'Nairobi',
        'has_children': True
    })
    assert response.status_code == 201

def test_upload_evidence(auth_client):
    from django.core.files.uploadedfile import SimpleUploadedFile
    file = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    response = auth_client.post('/api/vault/documents/', {
        'file': file,
        'file_type': 'image',
        'description': 'Test evidence',
        'incident_date': '2024-01-15T10:00:00'
    }, format='multipart')
    assert response.status_code == 201

def test_legal_bot_ask(client):
    response = client.post('/api/legal/ask/', {
        'question': 'What are my rights?',
        'session_id': 'test123'
    })
    assert response.status_code == 200

def test_privacy_policy(client):
    response = client.get('/api/privacy-policy/current/')
    assert response.status_code == 200

def test_county_rankings(client):
    response = client.get('/api/scorecard/rankings/')
    assert response.status_code == 200
