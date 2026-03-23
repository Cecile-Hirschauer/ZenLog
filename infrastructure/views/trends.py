from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.services.tracking_service import TrackingService
from infrastructure.permissions.roles import IsPatient
from infrastructure.repositories.indicator_repository import DjangoIndicatorRepository
from infrastructure.repositories.wellness_entry_repository import (
    DjangoWellnessEntryRepository,
)
from infrastructure.serializers.wellness import TrendSerializer


class TrendView(APIView):
    """GET /api/wellness/trends/?period=7&indicator_id=<uuid>

    Returns aggregated trend data for the authenticated patient.
    """

    permission_classes = [IsAuthenticated, IsPatient]

    def get(self, request):
        period = int(request.query_params.get("period", 7))
        indicator_id = request.query_params.get("indicator_id")

        if not indicator_id:
            return Response(
                {"detail": "indicator_id query parameter is required."},
                status=400,
            )

        service = TrackingService(
            entry_repo=DjangoWellnessEntryRepository(),
            indicator_repo=DjangoIndicatorRepository(),
        )

        trend = service.compute_trend(
            patient_id=str(request.user.id),
            indicator_id=indicator_id,
            period_days=period,
        )

        return Response(TrendSerializer(trend).data)
