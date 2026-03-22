from datetime import date, timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.infrastructure.factories import (
    AdminFactory,
    CoachFactory,
    IndicatorFactory,
    UserFactory,
    WellnessEntryFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def patient():
    user = UserFactory(email="patient@zenlog.test")
    user.set_password("TestPass123!")
    user.save()
    return user


@pytest.fixture
def admin_user():
    user = AdminFactory(email="admin@zenlog.test")
    user.set_password("TestPass123!")
    user.save()
    return user


@pytest.fixture
def auth_client(api_client, patient):
    """APIClient authenticated as patient."""
    response = api_client.post(
        "/api/auth/token/",
        {"email": patient.email, "password": "TestPass123!"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """APIClient authenticated as admin."""
    response = api_client.post(
        "/api/auth/token/",
        {"email": admin_user.email, "password": "TestPass123!"},
        format="json",
    )
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client


class TestCreateEntry:
    """T-I-07, T-I-08: Create wellness entry."""

    def test_create_entry_success(self, auth_client, patient):
        """T-I-07: Patient creates a valid entry."""
        indicator = IndicatorFactory(name="mood", min_value=1, max_value=10)

        response = auth_client.post(
            "/api/wellness/entries/",
            {
                "indicator_id": str(indicator.id),
                "date": str(date.today()),
                "value": 7.0,
                "note": "Good day",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == 7.0
        assert response.data["note"] == "Good day"
        assert response.data["patient_id"] == str(patient.id)

    def test_create_duplicate_entry(self, auth_client, patient):
        """T-I-08: Duplicate entry returns 400."""
        indicator = IndicatorFactory(name="sleep")
        WellnessEntryFactory(
            patient=patient, indicator=indicator, date=date.today()
        )

        response = auth_client.post(
            "/api/wellness/entries/",
            {
                "indicator_id": str(indicator.id),
                "date": str(date.today()),
                "value": 8.0,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestListEntries:
    """T-I-09, T-I-10: List and detail entries."""

    def test_list_own_entries(self, auth_client, patient):
        """T-I-09: Patient sees only their own entries."""
        indicator = IndicatorFactory()
        WellnessEntryFactory(patient=patient, indicator=indicator, value=7.0)
        WellnessEntryFactory(patient=patient, indicator=indicator, value=8.0,
                             date=date.today() - timedelta(days=1))
        # Another patient's entry
        WellnessEntryFactory(indicator=indicator, value=5.0)

        response = auth_client.get("/api/wellness/entries/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_cannot_see_other_patient_entry(self, auth_client):
        """T-I-10: Accessing another patient's entry returns 404."""
        other_entry = WellnessEntryFactory()

        response = auth_client.get(f"/api/wellness/entries/{other_entry.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateEntry:
    """T-I-11: Update entry."""

    def test_update_own_entry(self, auth_client, patient):
        """T-I-11: Patient updates their own entry."""
        indicator = IndicatorFactory()
        entry = WellnessEntryFactory(
            patient=patient, indicator=indicator, value=5.0
        )

        response = auth_client.patch(
            f"/api/wellness/entries/{entry.id}/",
            {"value": 8.0, "note": "Updated"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["value"] == 8.0
        assert response.data["note"] == "Updated"


class TestTrends:
    """T-I-12: Trends endpoint."""

    def test_trends_7_days(self, auth_client, patient):
        """T-I-12: Trends returns average for period."""
        indicator = IndicatorFactory()
        for i in range(5):
            WellnessEntryFactory(
                patient=patient,
                indicator=indicator,
                date=date.today() - timedelta(days=i),
                value=float(6 + i),
            )

        response = auth_client.get(
            f"/api/wellness/trends/?period=7&indicator_id={indicator.id}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["entry_count"] == 5
        assert response.data["average"] is not None


class TestIndicators:
    """T-I-13: List indicators."""

    def test_list_active_indicators(self, auth_client):
        """T-I-13: Patient sees only active indicators."""
        IndicatorFactory(name="mood", is_active=True)
        IndicatorFactory(name="sleep", is_active=True)
        IndicatorFactory(name="deprecated", is_active=False)

        response = auth_client.get("/api/wellness/indicators/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2