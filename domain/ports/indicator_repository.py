from abc import ABC, abstractmethod

from domain.entities.indicator import Indicator


class IndicatorRepository(ABC):
    """Abstract repository for Indicator persistence."""

    @abstractmethod
    def find_by_id(self, indicator_id: str) -> Indicator | None:
        """Find an indicator by its ID.

        Returns:
            The Indicator if found, None otherwise.
        """
        pass

    @abstractmethod
    def find_all_active(self) -> list[Indicator]:
        """Find all active indicators.

        Returns:
            List of indicators where is_active is True.
        """
        pass

    @abstractmethod
    def save(self, indicator: Indicator) -> Indicator:
        """Persist an indicator (create or update).

        Returns:
            The saved Indicator.
        """
        pass
