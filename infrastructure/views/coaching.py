from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.services.coaching_service import CoachingService
from infrastructure.permissions.roles import IsCoach
from infrastructure.repositories.assignment_repository import DjangoAssignmentRepository
from infrastructure.repositories.wellness_entry_repository import (
    DjangoWellnessEntryRepository,
)
from infrastructure.serializers.coaching import PatientEntrySerializer


class CoachingPatientsView(APIView):
    """GET /api/coaching/patients/ — List patients assigned to the coach."""

    permission_classes = [IsAuthenticated, IsCoach]

    def get_service(self) -> CoachingService:
        return CoachingService(
            assignment_repo=DjangoAssignmentRepository(),
            entry_reader=DjangoWellnessEntryRepository(),
        )

    def get(self, request):
        service = self.get_service()
        patient_ids = service.get_patient_list(str(request.user.id))
        return Response({"patients": patient_ids})


class CoachingPatientEntriesView(APIView):
    """GET /api/coaching/patients/{patient_id}/entries/ — Read patient data."""

    permission_classes = [IsAuthenticated, IsCoach]

    def get_service(self) -> CoachingService:
        return CoachingService(
            assignment_repo=DjangoAssignmentRepository(),
            entry_reader=DjangoWellnessEntryRepository(),
        )

    def get(self, request, patient_id):
        service = self.get_service()
        try:
            entries = service.get_patient_data(
                coach_id=str(request.user.id),
                patient_id=str(patient_id),
            )
        except PermissionError:
            return Response(
                {"detail": "No active assignment to this patient."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PatientEntrySerializer(entries, many=True)
        return Response({"results": serializer.data})
