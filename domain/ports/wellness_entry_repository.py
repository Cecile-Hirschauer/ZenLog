from abc import ABC, abstractmethod
from datetime import date

from domain.entities.wellness_entry import WellnessEntry


class WellnessEntryRepository(ABC):
    @abstractmethod
    def save(self, entry: WellnessEntry) -> WellnessEntry:
        pass

    @abstractmethod
    def find_by_id(self, entry_id: str) -> WellnessEntry | None:
        pass

    @abstractmethod
    def find_by_patient(
        self,
        patient_id: str,
        indicator_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[WellnessEntry]:
        pass

    @abstractmethod
    def exists(self, patient_id: str, indicator_id: str, date: date) -> bool:
        pass
