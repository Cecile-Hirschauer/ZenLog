from dataclasses import dataclass
from datetime import date


@dataclass
class WellnessEntry:
    id: str
    patient_id: str
    indicator_id: str
    date: date
    value: float
    note: str | None = None

    def is_owned_by(self, patient_id: str) -> bool:
        return self.patient_id == patient_id
