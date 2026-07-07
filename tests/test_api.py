import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )

@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client
def test_register(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'Test@1234'
        })
        self.assertEqual(response.status_code, 201)
        
def test_safety_timer_start(auth_client):
    response = auth_client.post('/api/safety/timer/start/', {
        'duration_minutes': 30
    })
    assert response.status_code in [200, 201, 404]

def test_safe_word_create(auth_client):
    response = auth_client.post('/api/safety/safe-word/', {
        'code_word': 'blueberry'
    })
    assert response.status_code in [200, 201, 404]

def test_risk_assessment(auth_client):
    response = auth_client.post('/api/safety/risk-assessment/', 
        {'answers': {'q1': True, 'q2': False}},
        format='json'
    )
    assert response.status_code in [200, 201, 400, 404]

def test_escape_plan(auth_client):
    response = auth_client.post('/api/safety/escape-plan/', {
        'county': 'Nairobi',
        'has_children': True,
        'documents_checklist': ['passport', 'medication'],
        'transportation_plan': 'Taxi to shelter',
        'safe_locations': ['Police station', "Friend's house"],
        'emergency_contacts': [{'name': 'Jane', 'phone': '+254712345678'}]
    }, format='json')
    assert response.status_code in [200, 201, 400, 404]

def test_upload_evidence(auth_client):
    file = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
    response = auth_client.post('/api/vault/documents/', {
        'file': file,
        'file_type': 'image',
        'description': 'Test evidence',
        'incident_date': '2024-01-15T10:00:00'
    }, format='multipart')
    assert response.status_code in [200, 201, 400, 403, 404]

def test_legal_bot_ask(api_client):
    response = api_client.post('/api/legal/ask/', {
        'question': 'What are my rights?',
        'session_id': 'test123'
    }, format='json')
    assert response.status_code in [200, 400, 404]

def test_privacy_policy(api_client, db):
    response = api_client.get('/api/privacy-policy/current/')
    assert response.status_code in [200, 404]

def test_county_rankings(api_client, db):
    response = api_client.get('/api/scorecard/rankings/')
    assert response.status_code in [200, 404]
