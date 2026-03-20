from datetime import date

from domain.entities.wellness_entry import WellnessEntry
from domain.ports.patient_entry_reader import PatientEntryReader
from domain.ports.wellness_entry_repository import WellnessEntryRepository
from infrastructure.models import WellnessEntry as WellnessEntryModel


class DjangoWellnessEntryRepository(WellnessEntryRepository, PatientEntryReader):
    """Django ORM adapter implementing both WellnessEntryRepository and PatientEntryReader.

    Single class, two contracts:
    - TrackingService receives it typed as WellnessEntryRepository (full CRUD)
    - CoachingService receives it typed as PatientEntryReader (read-only)
    """

    def save(self, entry: WellnessEntry) -> WellnessEntry:
        model, created = WellnessEntryModel.objects.update_or_create(
            id=entry.id,
            defaults={
                "patient_id": entry.patient_id,
                "indicator_id": entry.indicator_id,
                "date": entry.date,
                "value": entry.value,
                "note": entry.note,
            },
        )
        return self._to_entity(model)

    def find_by_id(self, entry_id: str) -> WellnessEntry | None:
        try:
            model = WellnessEntryModel.objects.get(id=entry_id)
            return self._to_entity(model)
        except WellnessEntryModel.DoesNotExist:
            return None

    def find_by_patient(
        self,
        patient_id: str,
        indicator_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[WellnessEntry]:
        qs = WellnessEntryModel.objects.filter(patient_id=patient_id)

        if indicator_id is not None:
            qs = qs.filter(indicator_id=indicator_id)
        if date_from is not None:
            qs = qs.filter(date__gte=date_from)
        if date_to is not None:
            qs = qs.filter(date__lte=date_to)

        return [self._to_entity(model) for model in qs]

    def exists(self, patient_id: str, indicator_id: str, date: date) -> bool:
        return WellnessEntryModel.objects.filter(
            patient_id=patient_id,
            indicator_id=indicator_id,
            date=date,
        ).exists()

    @staticmethod
    def _to_entity(model: WellnessEntryModel) -> WellnessEntry:
        """Convert Django model to domain entity."""
        return WellnessEntry(
            id=str(model.id),
            patient_id=str(model.patient_id),
            indicator_id=str(model.indicator_id),
            date=model.date,
            value=model.value,
            note=model.note,
        )
