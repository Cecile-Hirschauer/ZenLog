from abc import ABC, abstractmethod
from datetime import date

from domain.entities.wellness_entry import WellnessEntry


class WellnessEntryRepository(ABC):
    """Abstract repository for WellnessEntry persistence."""

    @abstractmethod
    def save(self, entry: WellnessEntry) -> WellnessEntry:
        """Persist a wellness entry (create or update).

        Returns:
            The saved WellnessEntry.
        """
        pass

    @abstractmethod
    def find_by_id(self, entry_id: str) -> WellnessEntry | None:
        """Find an entry by its ID.

        Returns:
            The WellnessEntry if found, None otherwise.
        """
        pass

    @abstractmethod
    def find_by_patient(
        self,
        patient_id: str,
        indicator_id: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[WellnessEntry]:
        """Find entries for a patient with optional filters.

        Args:
            patient_id: ID of the patient.
            indicator_id: Filter by indicator (optional).
            date_from: Filter entries on or after this date (optional).
            date_to: Filter entries on or before this date (optional).

        Returns:
            List of matching WellnessEntry objects.
        """
        pass

    @abstractmethod
    def exists(self, patient_id: str, indicator_id: str, date: date) -> bool:
        """Check if an entry exists for the given patient, indicator, and date.

        Returns:
            True if an entry exists, False otherwise.
        """
        pass
