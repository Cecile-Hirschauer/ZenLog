from dataclasses import dataclass


@dataclass
class Trend:
    """Value object representing aggregated wellness data over a period."""

    patient_id: str
    indicator_id: str
    period_days: int
    average: float | None
    entry_count: int
