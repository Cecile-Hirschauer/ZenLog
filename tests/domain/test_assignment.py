from datetime import date

from domain.entities.assignment import Assignment


class TestAssignment:
    """Tests T-D-20, T-D-21 from test plan"""

    def test_active_assignment_is_currently_active(self):
        """T-D-20: Active assignment returns True"""
        assignment = Assignment(
            id="assign-1",
            coach_id="coach-1",
            patient_id="patient-1",
            start_date=date(2026, 1, 1),
            is_active=True,
        )
        assert assignment.is_currently_active() is True

    def test_inactive_assignment_is_not_active(self):
        """T-D-21: Inactive assignment returns False"""
        assignment = Assignment(
            id="assign-1",
            coach_id="coach-1",
            patient_id="patient-1",
            start_date=date(2026, 1, 1),
            is_active=False,
            end_date=date(2026, 3, 1),
        )
        assert assignment.is_currently_active() is False

    def test_deactivate_sets_inactive_and_end_date(self):
        """T-D-15: Deactivation sets is_active=False and end_date"""
        assignment = Assignment(
            id="assign-1",
            coach_id="coach-1",
            patient_id="patient-1",
            start_date=date(2026, 1, 1),
            is_active=True,
        )
        assignment.deactivate(end_date=date(2026, 3, 19))

        assert assignment.is_active is False
        assert assignment.end_date == date(2026, 3, 19)
