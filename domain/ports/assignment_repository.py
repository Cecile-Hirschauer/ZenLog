from abc import ABC, abstractmethod

from domain.entities.assignment import Assignment


class AssignmentRepository(ABC):
    @abstractmethod
    def save(self, assignment: Assignment) -> Assignment:
        pass

    @abstractmethod
    def find_active_by_coach(self, coach_id: str) -> list[Assignment]:
        pass

    @abstractmethod
    def find_active_by_coach_and_patient(
        self, coach_id: str, patient_id: str
    ) -> Assignment | None:
        pass

    @abstractmethod
    def exists_active(self, coach_id: str, patient_id: str) -> bool:
        pass
