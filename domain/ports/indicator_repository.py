from abc import ABC, abstractmethod

from domain.entities.indicator import Indicator


class IndicatorRepository(ABC):
    @abstractmethod
    def find_by_id(self, indicator_id: str) -> Indicator | None:
        pass

    @abstractmethod
    def find_all_active(self) -> list[Indicator]:
        pass

    @abstractmethod
    def save(self, indicator: Indicator) -> Indicator:
        pass
