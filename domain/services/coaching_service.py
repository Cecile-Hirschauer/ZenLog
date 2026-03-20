from domain.entities.wellness_entry import WellnessEntry
from domain.ports.assignment_repository import AssignmentRepository
from domain.ports.patient_entry_reader import PatientEntryReader


class CoachingService:
    """Service for coach access to patient wellness data.

    Manages read-only access to patient data based on active assignments.
    Coaches can only view data from patients they are assigned to.
    """

    def __init__(
        self,
        assignment_repo: AssignmentRepository,
        entry_reader: PatientEntryReader,
    ):
        self.assignment_repo = assignment_repo
        self.entry_reader = entry_reader

    def check_access(self, coach_id: str, patient_id: str) -> bool:
        """Check if coach has an active assignment to the patient.

        Args:
            coach_id: ID of the coach.
            patient_id: ID of the patient.

        Returns:
            True if an active assignment exists, False otherwise.
        """
        return self.assignment_repo.exists_active(coach_id, patient_id)

    def get_patient_list(self, coach_id: str) -> list[str]:
        """Get list of patient IDs assigned to this coach.

        Args:
            coach_id: ID of the coach.

        Returns:
            List of patient IDs with active assignments to this coach.
        """
        assignments = self.assignment_repo.find_active_by_coach(coach_id)
        return [a.patient_id for a in assignments]

    def get_patient_data(self, coach_id: str, patient_id: str) -> list[WellnessEntry]:
        """Get wellness entries for a patient (read-only).

        Args:
            coach_id: ID of the coach requesting access.
            patient_id: ID of the patient whose data is requested.

        Returns:
            List of wellness entries for the patient.

        Raises:
            PermissionError: If coach has no active assignment to patient.
        """
        if not self.check_access(coach_id, patient_id):
            raise PermissionError(
                f"Coach {coach_id} has no active assignment to patient {patient_id}"
            )
        return self.entry_reader.find_by_patient(patient_id)
