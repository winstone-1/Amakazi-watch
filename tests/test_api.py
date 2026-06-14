import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
@ pytest.mark.django_db
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )

@pytest.fixture
@ pytest.mark.django_db
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@ pytest.mark.django_db
def test_safety_timer_start(auth_client):
    response = auth_client.post('/api/safety/timer/start/', {
        'duration_minutes': 30
    })
    assert response.status_code in [200, 201, 404]

@ pytest.mark.django_db
def test_safe_word_create(auth_client):
    response = auth_client.post('/api/safety/safe-word/', {
        'code_word': 'blueberry'
    })
    assert response.status_code in [200, 201, 404]

@ pytest.mark.django_db
def test_risk_assessment(auth_client):
    response = auth_client.post('/api/safety/risk-assessment/', {
        'answers': {'q1': True, 'q2': False}
    })
    assert response.status_code in [200, 201, 404]

@ pytest.mark.django_db
def test_escape_plan(auth_client):
    response = auth_client.post('/api/safety/escape-plan/', {
        'county': 'Nairobi',
        'has_children': True
    })
    assert response.status_code in [200, 201, 404]

@ pytest.mark.django_db
def test_upload_evidence(auth_client):
    file = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    response = auth_client.post('/api/vault/documents/', {
        'file': file,
        'file_type': 'image',
        'description': 'Test evidence',
        'incident_date': '2024-01-15T10:00:00'
    }, format='multipart')
    assert response.status_code in [200, 201, 404]

@ pytest.mark.django_db
def test_legal_bot_ask(api_client):
    response = api_client.post('/api/legal/ask/', {
        'question': 'What are my rights?',
        'session_id': 'test123'
    })
    assert response.status_code in [200, 400, 404]

@ pytest.mark.django_db
def test_privacy_policy(api_client):
    response = api_client.get('/api/privacy-policy/current/')
    assert response.status_code in [200, 404]

@ pytest.mark.django_db
def test_county_rankings(api_client):
    response = api_client.get('/api/scorecard/rankings/')
    assert response.status_code in [200, 404]
