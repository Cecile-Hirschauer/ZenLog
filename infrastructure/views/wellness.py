from datetime import date as date_type

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from domain.services.tracking_service import TrackingService
from infrastructure.permissions.roles import IsPatient
from infrastructure.repositories.indicator_repository import DjangoIndicatorRepository
from infrastructure.repositories.wellness_entry_repository import (
    DjangoWellnessEntryRepository,
)
from infrastructure.serializers.wellness import (
    CreateEntrySerializer,
    EntrySerializer,
    UpdateEntrySerializer,
)


class WellnessEntryViewSet(viewsets.ViewSet):
    """CRUD endpoints for patient wellness entries.

    All actions are scoped to the authenticated patient.
    Delegates business logic to TrackingService (domain layer).
    """

    permission_classes = [IsAuthenticated, IsPatient]

    def get_service(self) -> TrackingService:
        return TrackingService(
            entry_repo=DjangoWellnessEntryRepository(),
            indicator_repo=DjangoIndicatorRepository(),
        )

    @staticmethod
    def _parse_date(value):
        """Parse a date string (YYYY-MM-DD) or return None if invalid."""
        if not value:
            return None
        try:
            return date_type.fromisoformat(value)
        except (ValueError, TypeError):
            return None

    def list(self, request):
        """GET /api/wellness/entries/ — List my entries (with optional filters)."""
        repo = DjangoWellnessEntryRepository()
        entries = repo.find_by_patient(
            patient_id=str(request.user.id),
            indicator_id=request.query_params.get("indicator_id"),
            date_from=self._parse_date(request.query_params.get("date_from")),
            date_to=self._parse_date(request.query_params.get("date_to")),
        )
        # Manual pagination
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        start = (page - 1) * page_size
        end = start + page_size
        paginated = entries[start:end]

        serializer = EntrySerializer(paginated, many=True)
        return Response(
            {
                "count": len(entries),
                "results": serializer.data,
            }
        )

    def retrieve(self, request, pk=None):
        """GET /api/wellness/entries/{id}/ — Detail of one entry (owner only)."""
        repo = DjangoWellnessEntryRepository()
        entry = repo.find_by_id(pk)

        if entry is None or entry.patient_id != str(request.user.id):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(EntrySerializer(entry).data)

    def create(self, request):
        """POST /api/wellness/entries/ — Create a new entry."""
        serializer = CreateEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = self.get_service()
        try:
            entry = service.create_entry(
                patient_id=str(request.user.id),
                indicator_id=str(serializer.validated_data["indicator_id"]),
                entry_date=serializer.validated_data["date"],
                value=serializer.validated_data["value"],
                note=serializer.validated_data.get("note"),
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(EntrySerializer(entry).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /api/wellness/entries/{id}/ — Update an entry (owner only)."""
        serializer = UpdateEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = self.get_service()
        try:
            entry = service.update_entry(
                patient_id=str(request.user.id),
                entry_id=pk,
                value=serializer.validated_data.get("value"),
                note=serializer.validated_data.get("note"),
            )
        except PermissionError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(EntrySerializer(entry).data)
