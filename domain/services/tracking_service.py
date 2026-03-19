import uuid
from datetime import date

from domain.entities.wellness_entry import WellnessEntry
from domain.ports.indicator_repository import IndicatorRepository
from domain.ports.wellness_entry_repository import WellnessEntryRepository


class TrackingService:
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
        # Check duplicate
        if self.entry_repo.exists(patient_id, indicator_id, entry_date):
            raise ValueError(
                f"Entry already exists for patient {patient_id}, "
                f"indicator {indicator_id} on {entry_date}"
            )

        # Validate range
        indicator = self.indicator_repo.find_by_id(indicator_id)
        if not indicator.is_value_in_range(value):
            raise ValueError(
                f"Value {value} is out of range "
                f"[{indicator.min_value}, {indicator.max_value}]"
            )

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
        entry = self.entry_repo.find_by_id(entry_id)

        if not entry.is_owned_by(patient_id):
            raise PermissionError("Cannot update another patient's entry")

        if value is not None:
            indicator = self.indicator_repo.find_by_id(entry.indicator_id)
            if not indicator.is_value_in_range(value):
                raise ValueError(
                    f"Value {value} is out of range "
                    f"[{indicator.min_value}, {indicator.max_value}]"
                )
            entry.value = value

        if note is not None:
            entry.note = note

        return self.entry_repo.save(entry)
