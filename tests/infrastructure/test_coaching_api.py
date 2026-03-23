import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.infrastructure.factories import (
    AssignmentFactory,
    CoachFactory,
    IndicatorFactory,
    UserFactory,
    WellnessEntryFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


def _auth(api_client, user):
    """Helper: authenticate user via JWT and set credentials."""
    user.set_password("TestPass123!")
    user.save()
    response = api_client.post(
        "/api/auth/token/",
        {"email": user.email, "password": "TestPass123!"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


class TestCoachPatientList:
    """T-I-14, T-I-15: Coach retrieves assigned patients."""

    def test_coach_sees_assigned_patients(self, api_client):
        """T-I-14: GET /api/coaching/patients/ returns assigned patient IDs."""
        coach = CoachFactory()
        patient_a = UserFactory(email="pa@zenlog.test")
        patient_b = UserFactory(email="pb@zenlog.test")
        AssignmentFactory(coach=coach, patient=patient_a)
        AssignmentFactory(coach=coach, patient=patient_b)

        _auth(api_client, coach)
        response = api_client.get("/api/coaching/patients/")

        assert response.status_code == status.HTTP_200_OK
        patient_ids = response.data["patients"]
        assert str(patient_a.id) in patient_ids
        assert str(patient_b.id) in patient_ids

    def test_coach_sees_empty_list_without_assignments(self, api_client):
        """T-I-15: Coach with no assignments gets empty list."""
        coach = CoachFactory()
        _auth(api_client, coach)

        response = api_client.get("/api/coaching/patients/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["patients"] == []


class TestCoachPatientData:
    """T-I-16, T-I-17: Coach reads patient wellness data."""

    def test_coach_reads_assigned_patient_entries(self, api_client):
        """T-I-16: GET /api/coaching/patients/{id}/entries/ returns entries."""
        coach = CoachFactory()
        patient = UserFactory(email="cp@zenlog.test")
        indicator = IndicatorFactory()
        AssignmentFactory(coach=coach, patient=patient)
        WellnessEntryFactory(patient=patient, indicator=indicator, value=8.0)

        _auth(api_client, coach)
        response = api_client.get(f"/api/coaching/patients/{patient.id}/entries/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["value"] == 8.0

    def test_coach_cannot_read_unassigned_patient(self, api_client):
        """T-I-17: Coach without assignment to patient → 403."""
        coach = CoachFactory()
        patient = UserFactory(email="unassigned@zenlog.test")

        _auth(api_client, coach)
        response = api_client.get(f"/api/coaching/patients/{patient.id}/entries/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCoachPermissions:
    """T-I-18, T-I-19: Only coaches can access coaching endpoints."""

    def test_patient_cannot_access_coaching_endpoints(self, api_client):
        """T-I-18: Patient tries coaching endpoint → 403."""
        patient = UserFactory(email="sneaky@zenlog.test")
        _auth(api_client, patient)

        response = api_client.get("/api/coaching/patients/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_access_coaching(self, api_client):
        """T-I-19: No token → 401."""
        response = api_client.get("/api/coaching/patients/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
