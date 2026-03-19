from domain.entities.wellness_entry import WellnessEntry
from domain.ports.assignment_repository import AssignmentRepository
from domain.ports.wellness_entry_repository import WellnessEntryRepository


class CoachingService:
    def __init__(
        self,
        assignment_repo: AssignmentRepository,
        entry_repo: WellnessEntryRepository,
    ):
        self.assignment_repo = assignment_repo
        self.entry_repo = entry_repo

    def check_access(self, coach_id: str, patient_id: str) -> bool:
        """Check if coach has active assignment to patient."""
        return self.assignment_repo.exists_active(coach_id, patient_id)

    def get_patient_list(self, coach_id: str) -> list[str]:
        """Return list of patient IDs with active assignments to this coach."""
        assignments = self.assignment_repo.find_active_by_coach(coach_id)
        return [a.patient_id for a in assignments]

    def get_patient_data(self, coach_id: str, patient_id: str) -> list[WellnessEntry]:
        """Get patient wellness entries (read-only access for coach)."""
        if not self.check_access(coach_id, patient_id):
            raise PermissionError(
                f"Coach {coach_id} has no active assignment to patient {patient_id}"
            )
        return self.entry_repo.find_by_patient(patient_id)
