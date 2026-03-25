"""Trend value object for aggregated wellness statistics."""

from dataclasses import dataclass


@dataclass
class Trend:
    """Value object representing aggregated wellness data over a period.

    Attributes:
        patient_id: ID of the patient.
        indicator_id: ID of the tracked indicator.
        period_days: Number of days in the aggregation window.
        average: Computed average value, or None if no entries exist.
        entry_count: Number of entries in the period.
    """

    patient_id: str
    indicator_id: str
    period_days: int
    average: float | None
    entry_count: int
