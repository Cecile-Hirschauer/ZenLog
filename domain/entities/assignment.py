from dataclasses import dataclass
from datetime import date


@dataclass
class Assignment:
    id: str
    coach_id: str
    patient_id: str
    start_date: date
    is_active: bool = True
    end_date: date | None = None

    def is_currently_active(self) -> bool:
        return self.is_active

    def deactivate(self, end_date: date) -> None:
        self.is_active = False
        self.end_date = end_date
