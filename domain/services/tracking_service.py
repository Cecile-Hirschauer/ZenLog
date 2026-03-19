import uuid
from datetime import date

from domain.entities.indicator import Indicator
from domain.entities.wellness_entry import WellnessEntry
from domain.ports.indicator_repository import IndicatorRepository
from domain.ports.wellness_entry_repository import WellnessEntryRepository


class TrackingService:
    """Service for managing patient wellness entries.

    Handles creation and modification of daily wellness measurements,
    enforcing business rules like value range validation and duplicate prevention.
    """

    def __init__(
        self,
        entry_repo: WellnessEntryRepository,
        indicator_repo: IndicatorRepository,
    ):
        self.entry_repo = entry_repo
        self.indicator_repo = indicator_repo

    def create_entry(
        self,
        patient_id: str,
        indicator_id: str,
        entry_date: date,
        value: float,
        note: str | None = None,
    ) -> WellnessEntry:
        """Create a new wellness entry for a patient.

        Args:
            patient_id: ID of the patient creating the entry.
            indicator_id: ID of the indicator being tracked.
            entry_date: Date of the measurement.
            value: Measured value.
            note: Optional free-text note.

        Returns:
            The created WellnessEntry.

        Raises:
            ValueError: If entry already exists for this patient/indicator/date,
                or if value is outside the indicator's valid range.
        """
        if self.entry_repo.exists(patient_id, indicator_id, entry_date):
            raise ValueError(
                f"Entry already exists for patient {patient_id}, "
                f"indicator {indicator_id} on {entry_date}"
            )

        indicator = self.indicator_repo.find_by_id(indicator_id)
        self._validate_value(value, indicator)

        entry = WellnessEntry(
            id=str(uuid.uuid4()),
            patient_id=patient_id,
            indicator_id=indicator_id,
            date=entry_date,
            value=value,
            note=note,
        )

        return self.entry_repo.save(entry)

    def update_entry(
        self,
        patient_id: str,
        entry_id: str,
        value: float | None = None,
        note: str | None = None,
    ) -> WellnessEntry:
        """Update an existing wellness entry.

        Args:
            patient_id: ID of the patient requesting the update.
            entry_id: ID of the entry to update.
            value: New value (optional).
            note: New note (optional).

        Returns:
            The updated WellnessEntry.

        Raises:
            PermissionError: If patient does not own this entry.
            ValueError: If new value is outside the indicator's valid range.
        """
        entry = self.entry_repo.find_by_id(entry_id)

        if not entry.is_owned_by(patient_id):
            raise PermissionError("Cannot update another patient's entry")

        if value is not None:
            indicator = self.indicator_repo.find_by_id(entry.indicator_id)
            self._validate_value(value, indicator)
            entry.value = value

        if note is not None:
            entry.note = note

        return self.entry_repo.save(entry)

    def _validate_value(self, value: float, indicator: Indicator) -> None:
        """Validate that a value is within the indicator's allowed range.

        Raises:
            ValueError: If value is outside the valid range.
        """
        if not indicator.is_value_in_range(value):
            raise ValueError(
                f"Value {value} is out of range "
                f"[{indicator.min_value}, {indicator.max_value}]"
            )
