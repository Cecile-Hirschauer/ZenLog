from domain.entities.assignment import Assignment
from domain.ports.assignment_repository import AssignmentRepository
from infrastructure.models import Assignment as AssignmentModel


class DjangoAssignmentRepository(AssignmentRepository):
    """Django ORM adapter for AssignmentRepository."""

    def save(self, assignment: Assignment) -> Assignment:
        model, created = AssignmentModel.objects.update_or_create(
            id=assignment.id,
            defaults={
                "coach_id": assignment.coach_id,
                "patient_id": assignment.patient_id,
                "start_date": assignment.start_date,
                "end_date": assignment.end_date,
                "is_active": assignment.is_active,
            },
        )
        return self._to_entity(model)

    def find_active_by_coach(self, coach_id: str) -> list[Assignment]:
        qs = AssignmentModel.objects.filter(coach_id=coach_id, is_active=True)
        return [self._to_entity(model) for model in qs]

    def find_active_by_coach_and_patient(
        self, coach_id: str, patient_id: str
    ) -> Assignment | None:
        try:
            model = AssignmentModel.objects.get(
                coach_id=coach_id, patient_id=patient_id, is_active=True
            )
            return self._to_entity(model)
        except AssignmentModel.DoesNotExist:
            return None

    def exists_active(self, coach_id: str, patient_id: str) -> bool:
        return AssignmentModel.objects.filter(
            coach_id=coach_id, patient_id=patient_id, is_active=True
        ).exists()

    @staticmethod
    def _to_entity(model: AssignmentModel) -> Assignment:
        return Assignment(
            id=str(model.id),
            coach_id=str(model.coach_id),
            patient_id=str(model.patient_id),
            start_date=model.start_date,
            end_date=model.end_date,
            is_active=model.is_active,
        )
