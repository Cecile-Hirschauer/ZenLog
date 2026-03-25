"""Indicator entity representing a trackable wellness metric."""

from dataclasses import dataclass


@dataclass
class Indicator:
    """A wellness metric that patients can track.

    Attributes:
        id: Unique identifier.
        name: Display name (e.g., "mood", "sleep").
        unit: Measurement unit (e.g., "/10", "hours").
        min_value: Minimum allowed value.
        max_value: Maximum allowed value.
        is_active: Whether this indicator is available for tracking.
    """

    id: str
    name: str
    unit: str
    min_value: float
    max_value: float
    is_active: bool = True

    def is_value_in_range(self, value: float) -> bool:
        """Check if a value falls within the indicator's valid range."""
        return self.min_value <= value <= self.max_value
