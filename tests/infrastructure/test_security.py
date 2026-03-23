from datetime import timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from tests.infrastructure.factories import (
    CoachFactory,
    IndicatorFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


class TestAuthSecurity:
    """T-S-01, T-S-02: Authentication security tests."""

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


class TestRoleEscalation:
    """T-S-03, T-S-04: Role escalation tests."""

    def test_patient_cannot_create_indicator(self, api_client):
        """T-S-03: Patient tries to create indicator → 403."""
        patient = UserFactory(email="esc@zenlog.test")
        patient.set_password("TestPass123!")
        patient.save()

        response = api_client.post(
            "/api/auth/token/",
            {"email": "esc@zenlog.test", "password": "TestPass123!"},
            format="json",
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        response = api_client.post(
            "/api/wellness/indicators/",
            {"name": "hack", "unit": "x", "min_value": 0, "max_value": 10},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_coach_cannot_create_entry(self, api_client):
        """T-S-04: Coach tries to create wellness entry → 403."""
        coach = CoachFactory(email="coach-esc@zenlog.test")
        coach.set_password("TestPass123!")
        coach.save()

        response = api_client.post(
            "/api/auth/token/",
            {"email": "coach-esc@zenlog.test", "password": "TestPass123!"},
            format="json",
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        indicator = IndicatorFactory()
        response = api_client.post(
            "/api/wellness/entries/",
            {"indicator_id": str(indicator.id), "date": "2026-03-22", "value": 5},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestDataIsolation:
    """T-S-05: Cross-patient data access."""

    def test_patient_cannot_see_other_patient_entry(self, api_client):
        """T-S-05: Patient A accessing Patient B's entry → 404."""
        patient_a = UserFactory(email="a@zenlog.test")
        patient_a.set_password("TestPass123!")
        patient_a.save()

        from tests.infrastructure.factories import WellnessEntryFactory

        other_entry = WellnessEntryFactory()  # belongs to another patient

        response = api_client.post(
            "/api/auth/token/",
            {"email": "a@zenlog.test", "password": "TestPass123!"},
            format="json",
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        response = api_client.get(f"/api/wellness/entries/{other_entry.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestInjection:
    """T-S-08: SQL injection protection."""

    def test_sql_injection_in_date_filter(self, api_client):
        """T-S-08: SQL injection in query params is harmless."""
        patient = UserFactory(email="inj@zenlog.test")
        patient.set_password("TestPass123!")
        patient.save()

        response = api_client.post(
            "/api/auth/token/",
            {"email": "inj@zenlog.test", "password": "TestPass123!"},
            format="json",
        )
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        response = api_client.get("/api/wellness/entries/?date_from='; DROP TABLE--")

        # Should return 200 (empty list) or 400 — never a 500 SQL error
        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
        )
