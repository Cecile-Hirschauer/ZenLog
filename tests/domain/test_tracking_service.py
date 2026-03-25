"""Tests for the TrackingService domain service."""

from datetime import date
from unittest.mock import MagicMock

import pytest

from domain.entities.indicator import Indicator
from domain.entities.wellness_entry import WellnessEntry
from domain.services.tracking_service import TrackingService


@pytest.fixture
def mood_indicator():
    """Return a mood indicator with a 1-10 range."""
    return Indicator(
        id="ind-1",
        name="mood",
        unit="/10",
        min_value=1.0,
        max_value=10.0,
    )


@pytest.fixture
def entry_repo():
    """Return a mock WellnessEntryRepository."""
    return MagicMock()


@pytest.fixture
def indicator_repo(mood_indicator):
    """Return a mock IndicatorRepository pre-configured with mood_indicator."""
    repo = MagicMock()
    repo.find_by_id.return_value = mood_indicator
    return repo


@pytest.fixture
def service(entry_repo, indicator_repo):
    """Return a TrackingService wired with mock repositories."""
    return TrackingService(
        entry_repo=entry_repo,
        indicator_repo=indicator_repo,
    )


class TestCreateEntry:
    """Tests T-D-01 to T-D-04 from test plan"""

    def test_create_valid_entry(self, service, entry_repo):
        """T-D-01: Create a valid wellness entry"""
        entry_repo.exists.return_value = False
        entry_repo.save.side_effect = lambda e: e

        entry = service.create_entry(
            patient_id="patient-1",
            indicator_id="ind-1",
            entry_date=date(2026, 3, 19),
            value=7.0,
            note="Good day",
        )

        assert entry.patient_id == "patient-1"
        assert entry.value == 7.0
        assert entry.note == "Good day"
        entry_repo.save.assert_called_once()

    def test_reject_value_above_range(self, service, entry_repo):
        """T-D-02: Value above max raises ValueError"""
        entry_repo.exists.return_value = False

        with pytest.raises(ValueError, match="out of range"):
            service.create_entry(
                patient_id="patient-1",
                indicator_id="ind-1",
                entry_date=date(2026, 3, 19),
                value=11.0,
            )

    def test_reject_value_below_range(self, service, entry_repo):
        """T-D-03: Value below min raises ValueError"""
        entry_repo.exists.return_value = False

        with pytest.raises(ValueError, match="out of range"):
            service.create_entry(
                patient_id="patient-1",
                indicator_id="ind-1",
                entry_date=date(2026, 3, 19),
                value=0.0,
            )

    def test_reject_duplicate_entry(self, service, entry_repo):
        """T-D-04: Duplicate entry raises DuplicateEntryError"""
        entry_repo.exists.return_value = True

        with pytest.raises(Exception, match="already exists"):
            service.create_entry(
                patient_id="patient-1",
                indicator_id="ind-1",
                entry_date=date(2026, 3, 19),
                value=7.0,
            )


class TestUpdateEntry:
    """Tests T-D-05, T-D-06 from test plan"""

    def test_update_own_entry(self, service, entry_repo):
        """T-D-05: Patient can update their own entry"""
        existing = WellnessEntry(
            id="entry-1",
            patient_id="patient-1",
            indicator_id="ind-1",
            date=date(2026, 3, 19),
            value=5.0,
        )
        entry_repo.find_by_id.return_value = existing
        entry_repo.save.side_effect = lambda e: e

        updated = service.update_entry(
            patient_id="patient-1",
            entry_id="entry-1",
            value=8.0,
            note="Updated",
        )

        assert updated.value == 8.0
        assert updated.note == "Updated"

    def test_reject_update_by_other_patient(self, service, entry_repo):
        """T-D-06: Cannot update another patient's entry"""
        existing = WellnessEntry(
            id="entry-1",
            patient_id="patient-1",
            indicator_id="ind-1",
            date=date(2026, 3, 19),
            value=5.0,
        )
        entry_repo.find_by_id.return_value = existing

        with pytest.raises(PermissionError):
            service.update_entry(
                patient_id="patient-2",
                entry_id="entry-1",
                value=8.0,
            )
