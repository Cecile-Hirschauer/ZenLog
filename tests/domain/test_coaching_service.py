from datetime import date
from unittest.mock import MagicMock

import pytest

from domain.entities.assignment import Assignment
from domain.entities.wellness_entry import WellnessEntry
from domain.services.coaching_service import CoachingService


@pytest.fixture
def assignment_repo():
    return MagicMock()


@pytest.fixture
def entry_reader():
    return MagicMock()


@pytest.fixture
def service(assignment_repo, entry_reader):
    return CoachingService(
        assignment_repo=assignment_repo,
        entry_reader=entry_reader,
    )


class TestCheckAccess:
    """Tests T-D-11 to T-D-13 from test plan"""

    def test_access_granted_with_active_assignment(self, service, assignment_repo):
        """T-D-11: Coach can access patient with active assignment"""
        assignment_repo.exists_active.return_value = True

        assert service.check_access("coach-1", "patient-1") is True

    def test_access_denied_without_assignment(self, service, assignment_repo):
        """T-D-12: Coach cannot access patient without assignment"""
        assignment_repo.exists_active.return_value = False

        assert service.check_access("coach-1", "patient-1") is False

    def test_access_denied_with_inactive_assignment(self, service, assignment_repo):
        """T-D-13: Coach cannot access patient with inactive assignment"""
        assignment_repo.exists_active.return_value = False

        assert service.check_access("coach-1", "patient-1") is False


class TestGetPatientList:
    """Test T-D-14 from test plan"""

    def test_returns_only_active_patient_ids(self, service, assignment_repo):
        """T-D-14: Only active assignments are returned"""
        assignment_repo.find_active_by_coach.return_value = [
            Assignment(
                id="a1",
                coach_id="coach-1",
                patient_id="patient-1",
                start_date=date(2026, 1, 1),
                is_active=True,
            ),
            Assignment(
                id="a2",
                coach_id="coach-1",
                patient_id="patient-2",
                start_date=date(2026, 2, 1),
                is_active=True,
            ),
        ]

        patients = service.get_patient_list("coach-1")

        assert patients == ["patient-1", "patient-2"]


class TestGetPatientData:
    """Tests for coach reading patient entries"""

    def test_returns_entries_when_access_granted(
        self, service, assignment_repo, entry_reader
    ):
        """Coach gets patient data when assignment is active"""
        assignment_repo.exists_active.return_value = True
        entry_reader.find_by_patient.return_value = [
            WellnessEntry(
                id="e1",
                patient_id="patient-1",
                indicator_id="ind-1",
                date=date(2026, 3, 19),
                value=7.0,
            ),
        ]

        entries = service.get_patient_data("coach-1", "patient-1")

        assert len(entries) == 1
        assert entries[0].patient_id == "patient-1"

    def test_raises_when_access_denied(self, service, assignment_repo):
        """Coach cannot get data without active assignment"""
        assignment_repo.exists_active.return_value = False

        with pytest.raises(PermissionError):
            service.get_patient_data("coach-1", "patient-1")
