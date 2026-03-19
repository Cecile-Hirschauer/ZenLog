from abc import ABC, abstractmethod

from domain.entities.assignment import Assignment


class AssignmentRepository(ABC):
    """Abstract repository for Assignment persistence."""

    @abstractmethod
    def save(self, assignment: Assignment) -> Assignment:
        """Persist an assignment (create or update).

        Returns:
            The saved Assignment.
        """
        pass

    @abstractmethod
    def find_active_by_coach(self, coach_id: str) -> list[Assignment]:
        """Find all active assignments for a coach.

        Returns:
            List of active Assignment objects for the given coach.
        """
        pass

    @abstractmethod
    def find_active_by_coach_and_patient(
        self, coach_id: str, patient_id: str
    ) -> Assignment | None:
        """Find active assignment between a coach and patient.

        Returns:
            The Assignment if an active one exists, None otherwise.
        """
        pass

    @abstractmethod
    def exists_active(self, coach_id: str, patient_id: str) -> bool:
        """Check if an active assignment exists between coach and patient.

        Returns:
            True if an active assignment exists, False otherwise.
        """
        pass
