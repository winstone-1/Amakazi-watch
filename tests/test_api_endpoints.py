import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_register_saves_role_and_returns_user_payload():
    client = APIClient()
    response = client.post(
        "/api/auth/register/",
        {
            "username": "survivor1",
            "email": "survivor@example.com",
            "password": "strongpass123",
            "role": "survivor",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["user"]["role"] == "survivor"
    assert User.objects.get(username="survivor1").role == "survivor"


@pytest.mark.django_db
def test_token_endpoint_returns_role_in_user_payload():
    User.objects.create_user(
        username="tokenuser",
        email="token@example.com",
        password="strongpass123",
        role="counselor",
    )
    client = APIClient()
    response = client.post(
        "/api/auth/token/",
        {"username": "tokenuser", "password": "strongpass123"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "counselor"


@pytest.mark.django_db
def test_profile_can_be_read_and_updated():
    user = User.objects.create_user(
        username="profileuser",
        email="profile@example.com",
        password="strongpass123",
        role="survivor",
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/profile/")
    assert response.status_code == 200
    assert response.json()["role"] == "survivor"

    patch_response = client.patch(
        "/api/profile/",
        {"phone": "0712345678", "bio": "Updated bio", "role": "counselor"},
        format="json",
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["phone"] == "0712345678"
    assert patch_response.json()["bio"] == "Updated bio"
    assert patch_response.json()["role"] == "counselor"


@pytest.mark.django_db
def test_reports_can_be_created_and_listed_for_user():
    user = User.objects.create_user(
        username="reportuser",
        email="report@example.com",
        password="strongpass123",
        role="survivor",
    )
    client = APIClient()
    client.force_authenticate(user=user)

    create_response = client.post(
        "/api/reports/",
        {
            "abuse_type": "physical",
            "relationship": "partner",
            "county": "Nairobi",
            "sub_county": "Kibra",
            "description": "Test safety report",
            "phone": "0712345678",
            "is_anonymous": False,
        },
        format="json",
    )

    assert create_response.status_code == 201
    assert create_response.json()["user"] == user.id

    list_response = client.get("/api/reports/")
    assert list_response.status_code == 200
    assert list_response.json()[0]["user"] == user.id
