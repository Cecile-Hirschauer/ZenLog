"""Tests for the WellnessEntry entity."""

from datetime import date

from domain.entities.wellness_entry import WellnessEntry


class TestWellnessEntry:
    """Tests T-D-18, T-D-19 from test plan"""

    def _make_entry(self, patient_id="patient-1"):
        """Create a WellnessEntry fixture with sensible defaults."""
        return WellnessEntry(
            id="entry-1",
            patient_id=patient_id,
            indicator_id="ind-1",
            date=date(2026, 3, 19),
            value=7.0,
        )

    def test_is_owned_by_correct_patient(self):
        """T-D-18: Entry belongs to the patient who created it"""
        entry = self._make_entry(patient_id="patient-1")
        assert entry.is_owned_by("patient-1") is True

    def test_is_owned_by_wrong_patient(self):
        """T-D-19: Entry does not belong to another patient"""
        entry = self._make_entry(patient_id="patient-1")
        assert entry.is_owned_by("patient-2") is False

    def test_entry_created_with_no_note(self):
        """Default note is None"""
        entry = self._make_entry()
        assert entry.note is None

    def test_entry_created_with_note(self):
        """Note can be provided"""
        entry = WellnessEntry(
            id="entry-2",
            patient_id="patient-1",
            indicator_id="ind-1",
            date=date(2026, 3, 19),
            value=7.0,
            note="Bonne journée",
        )
        assert entry.note == "Bonne journée"
