from dataclasses import dataclass
from datetime import date


@dataclass
class WellnessEntry:
    """A daily wellness measurement recorded by a patient.

    Attributes:
        id: Unique identifier.
        patient_id: ID of the patient who owns this entry.
        indicator_id: ID of the indicator being tracked.
        date: Date of the measurement.
        value: Recorded value (must be within indicator's range).
        note: Optional free-text note.
    """

    id: str
    patient_id: str
    indicator_id: str
    date: date
    value: float
    note: str | None = None

    def is_owned_by(self, patient_id: str) -> bool:
        """Check if this entry belongs to the given patient."""
        return self.patient_id == patient_id
