"""Assignment entity representing a coach-patient relationship."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Assignment:
    """A coach-patient relationship with lifecycle management.

    Attributes:
        id: Unique identifier.
        coach_id: ID of the assigned coach.
        patient_id: ID of the assigned patient.
        start_date: Date when the assignment became active.
        is_active: Whether the coach currently has access to patient data.
        end_date: Date when the assignment was deactivated (if applicable).
    """

    id: str
    coach_id: str
    patient_id: str
    start_date: date
    is_active: bool = True
    end_date: date | None = None

    def is_currently_active(self) -> bool:
        """Check if this assignment is currently active."""
        return self.is_active

    def deactivate(self, end_date: date) -> None:
        """Deactivate the assignment, revoking coach access to patient data."""
        self.is_active = False
        self.end_date = end_date
