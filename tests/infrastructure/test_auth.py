import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.infrastructure.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


class TestRegister:
    """T-I-01, T-I-02: Registration endpoint."""

    def test_register_success(self, api_client):
        """T-I-01: Successful registration returns 201, no password in response."""
        payload = {
            "email": "new@zenlog.test",
            "username": "newuser",
            "password": "SecurePass123!",
            "role": "patient",
        }

        response = api_client.post("/api/auth/register/", payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in response.data
        assert "password_hash" not in response.data
        assert response.data["email"] == "new@zenlog.test"
        assert response.data["role"] == "patient"

    def test_register_duplicate_email(self, api_client):
        """T-I-02: Duplicate email returns 400."""
        UserFactory(email="dup@zenlog.test")

        payload = {
            "email": "dup@zenlog.test",
            "username": "another",
            "password": "SecurePass123!",
            "role": "patient",
        }

        response = api_client.post("/api/auth/register/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestToken:
    """T-I-03, T-I-04, T-I-05: JWT token endpoints."""

    def test_obtain_token_success(self, api_client):
        """T-I-03: Valid credentials return access + refresh tokens."""
        user = UserFactory(email="login@zenlog.test")
        user.set_password("SecurePass123!")
        user.save()

        response = api_client.post(
            "/api/auth/token/",
            {"email": "login@zenlog.test", "password": "SecurePass123!"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_wrong_password(self, api_client):
        """T-I-04: Wrong password returns 401."""
        user = UserFactory(email="wrong@zenlog.test")
        user.set_password("CorrectPass123!")
        user.save()

        response = api_client.post(
            "/api/auth/token/",
            {"email": "wrong@zenlog.test", "password": "BadPass"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self, api_client):
        """T-I-05: Valid refresh token returns new access token."""
        user = UserFactory(email="refresh@zenlog.test")
        user.set_password("SecurePass123!")
        user.save()

        # First obtain tokens
        token_response = api_client.post(
            "/api/auth/token/",
            {"email": "refresh@zenlog.test", "password": "SecurePass123!"},
            format="json",
        )
        refresh_token = token_response.data["refresh"]

        # Then refresh
        response = api_client.post(
            "/api/auth/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestUnauthenticatedAccess:
    """T-I-06: Unauthenticated access is blocked."""

    def test_access_without_token(self, api_client):
        """T-I-06: GET protected endpoint without token returns 401."""
        response = api_client.get("/api/wellness/entries/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED