from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.infrastructure.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


class TestRateLimiting:
    """T-S-06: Throttling on auth endpoints."""

    def test_login_throttled_after_limit(self, api_client):
        """T-S-06: Repeated login attempts are throttled."""
        from rest_framework.throttling import ScopedRateThrottle

        # Clear any previous throttle cache
        ScopedRateThrottle.cache.clear()

        with patch.object(ScopedRateThrottle, "get_rate", return_value="3/min"):
            user = UserFactory(email="throttle@zenlog.test")
            user.set_password("TestPass123!")
            user.save()

            # Burn through the 3 allowed requests
            for _ in range(3):
                api_client.post(
                    "/api/auth/token/",
                    {"email": "throttle@zenlog.test", "password": "wrong"},
                    format="json",
                )

            # 4th request should be throttled
            response = api_client.post(
                "/api/auth/token/",
                {"email": "throttle@zenlog.test", "password": "wrong"},
                format="json",
            )

            assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


class TestSecurityHeaders:
    """T-S-07: Security headers are present."""

    def test_response_has_security_headers(self, api_client):
        """T-S-07: API responses include key security headers."""
        response = api_client.get("/api/auth/token/")

        # X-Content-Type-Options set by SecurityMiddleware
        assert response.get("X-Content-Type-Options") == "nosniff"
        # X-Frame-Options set by XFrameOptionsMiddleware
        assert response.get("X-Frame-Options") in ("DENY", "SAMEORIGIN")


class TestCORS:
    """CORS is configured and restrictive."""

    def test_cors_rejects_unknown_origin(self, api_client):
        """Preflight from unknown origin is not allowed."""
        response = api_client.options(
            "/api/wellness/entries/",
            HTTP_ORIGIN="https://evil.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )

        # Should NOT have Access-Control-Allow-Origin for evil.com
        allow_origin = response.get("Access-Control-Allow-Origin")
        assert allow_origin != "https://evil.com"

    def test_cors_allows_configured_origin(self, api_client, settings):
        """Preflight from allowed origin gets CORS headers."""
        settings.CORS_ALLOWED_ORIGINS = ["https://zenlog.app"]

        response = api_client.options(
            "/api/wellness/entries/",
            HTTP_ORIGIN="https://zenlog.app",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )

        assert response.get("Access-Control-Allow-Origin") == "https://zenlog.app"


class TestInputValidation:
    """Extra input validation hardening."""

    def test_register_rejects_weak_password(self, api_client):
        """Registration with a weak password is rejected."""
        response = api_client.post(
            "/api/auth/register/",
            {
                "email": "weak@zenlog.test",
                "username": "weakuser",
                "password": "123",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_rejects_invalid_email(self, api_client):
        """Registration with malformed email is rejected."""
        response = api_client.post(
            "/api/auth/register/",
            {
                "email": "not-an-email",
                "username": "bademail",
                "password": "StrongPass123!",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST