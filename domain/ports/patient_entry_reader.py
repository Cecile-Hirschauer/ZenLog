from abc import ABC, abstractmethod
from datetime import date

from domain.entities.wellness_entry import WellnessEntry


class PatientEntryReader(ABC):
    """Read-only access to patient wellness entries.

    This port belongs to the Coaching bounded context.
    It enforces read-only access at the domain level,
    ensuring coaches can never write patient data through this interface.
    """

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
