from dataclasses import dataclass


@dataclass
class Indicator:
    id: str
    name: str
    unit: str
    min_value: float
    max_value: float
    is_active: bool = True

    def is_value_in_range(self, value: float) -> bool:
        return self.min_value <= value <= self.max_value
