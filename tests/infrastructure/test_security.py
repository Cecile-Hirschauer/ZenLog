from datetime import timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from tests.infrastructure.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


class TestAuthSecurity:
    """T-S-01, T-S-02: Authentication security tests."""

    @pytest.mark.skip(
        reason="Endpoint /api/wellness/entries/ not yet implemented (Phase 3)"
    )
    def test_access_without_token(self, api_client):
        """T-S-01: Request without token returns 401."""
        response = api_client.get("/api/wellness/entries/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_access_with_expired_token(self, api_client):
        """T-S-02: Request with expired token returns 401."""
        user = UserFactory()

        # Create a token that's already expired
        token = AccessToken.for_user(user)
        token.set_exp(lifetime=-timedelta(seconds=1))

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        response = api_client.get("/api/wellness/entries/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
