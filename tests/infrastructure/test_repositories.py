from datetime import date, timedelta

from tests.infrastructure.factories import (
    AssignmentFactory,
    CoachFactory,
    IndicatorFactory,
    UserFactory,
    WellnessEntryFactory,
)


class TestDjangoWellnessEntryRepository:
    """T-R-01 to T-R-03: WellnessEntry repository adapter tests."""

    def test_save_and_find_by_id(self):
        """T-R-01: Entry is persisted and retrievable by find_by_id."""
        patient = UserFactory()
        indicator = IndicatorFactory()
        entry = WellnessEntryFactory(patient=patient, indicator=indicator, value=7.0)

        from infrastructure.repositories.wellness_entry_repository import (
            DjangoWellnessEntryRepository,
        )

        repo = DjangoWellnessEntryRepository()
        result = repo.find_by_id(str(entry.id))

        assert result is not None
        assert result.patient_id == str(patient.id)
        assert result.value == 7.0

    def test_find_by_patient_with_filters(self):
        """T-R-02: find_by_patient filters by patient, indicator, date range."""
        patient = UserFactory()
        indicator_a = IndicatorFactory(name="mood")
        indicator_b = IndicatorFactory(name="sleep")

        today = date.today()
        yesterday = today - timedelta(days=1)

        WellnessEntryFactory(
            patient=patient, indicator=indicator_a, date=today, value=8.0
        )
        WellnessEntryFactory(
            patient=patient, indicator=indicator_a, date=yesterday, value=6.0
        )
        WellnessEntryFactory(
            patient=patient, indicator=indicator_b, date=today, value=7.0
        )
        # Another patient's entry — should not appear
        WellnessEntryFactory(indicator=indicator_a, date=today, value=5.0)

        from infrastructure.repositories.wellness_entry_repository import (
            DjangoWellnessEntryRepository,
        )

        repo = DjangoWellnessEntryRepository()

        # All entries for patient
        results = repo.find_by_patient(str(patient.id))
        assert len(results) == 3

        # Filter by indicator
        results = repo.find_by_patient(
            str(patient.id), indicator_id=str(indicator_a.id)
        )
        assert len(results) == 2

        # Filter by date range
        results = repo.find_by_patient(str(patient.id), date_from=today, date_to=today)
        assert len(results) == 2

    def test_exists(self):
        """T-R-03: exists returns True for existing triplet."""
        entry = WellnessEntryFactory()

        from infrastructure.repositories.wellness_entry_repository import (
            DjangoWellnessEntryRepository,
        )

        repo = DjangoWellnessEntryRepository()

        assert (
            repo.exists(str(entry.patient.id), str(entry.indicator.id), entry.date)
            is True
        )
        assert (
            repo.exists(
                str(entry.patient.id),
                str(entry.indicator.id),
                entry.date + timedelta(days=1),
            )
            is False
        )


class TestDjangoIndicatorRepository:
    """T-R-04: Indicator repository adapter tests."""

    def test_find_all_active(self):
        """T-R-04: Only active indicators are returned."""
        IndicatorFactory(name="mood", is_active=True)
        IndicatorFactory(name="sleep", is_active=True)
        IndicatorFactory(name="deprecated", is_active=False)

        from infrastructure.repositories.indicator_repository import (
            DjangoIndicatorRepository,
        )

        repo = DjangoIndicatorRepository()
        results = repo.find_all_active()

        assert len(results) == 2
        assert all(i.is_active for i in results)


class TestDjangoAssignmentRepository:
    """T-R-05 to T-R-06: Assignment repository adapter tests."""

    def test_exists_active(self):
        """T-R-05: exists_active returns True for active assignment."""
        assignment = AssignmentFactory(is_active=True)

        from infrastructure.repositories.assignment_repository import (
            DjangoAssignmentRepository,
        )

        repo = DjangoAssignmentRepository()

        assert (
            repo.exists_active(str(assignment.coach.id), str(assignment.patient.id))
            is True
        )

        # Deactivate
        assignment.is_active = False
        assignment.save()

        assert (
            repo.exists_active(str(assignment.coach.id), str(assignment.patient.id))
            is False
        )

    def test_find_active_by_coach(self):
        """T-R-06: Only active assignments for the coach are returned."""
        coach = CoachFactory()
        AssignmentFactory(coach=coach, is_active=True)
        AssignmentFactory(coach=coach, is_active=True)
        AssignmentFactory(coach=coach, is_active=False)  # inactive
        AssignmentFactory(is_active=True)  # other coach

        from infrastructure.repositories.assignment_repository import (
            DjangoAssignmentRepository,
        )

        repo = DjangoAssignmentRepository()
        results = repo.find_active_by_coach(str(coach.id))

        assert len(results) == 2
