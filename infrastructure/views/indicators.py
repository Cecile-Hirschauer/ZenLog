import uuid

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from domain.entities.indicator import Indicator
from infrastructure.permissions.roles import IsAdmin
from infrastructure.repositories.indicator_repository import DjangoIndicatorRepository
from infrastructure.serializers.wellness import (
    CreateIndicatorSerializer,
    IndicatorSerializer,
)


class IndicatorViewSet(viewsets.ViewSet):
    """Endpoints for wellness indicators.

    GET (list): accessible to all authenticated users.
    POST (create): admin only.
    """

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def list(self, request):
        """GET /api/wellness/indicators/ — List active indicators."""
        repo = DjangoIndicatorRepository()
        indicators = repo.find_all_active()
        serializer = IndicatorSerializer(indicators, many=True)

        # Manual pagination for consistency
        return Response(
            {
                "count": len(indicators),
                "results": serializer.data,
            }
        )

    def create(self, request):
        """POST /api/wellness/indicators/ — Create indicator (admin only)."""
        serializer = CreateIndicatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        repo = DjangoIndicatorRepository()
        indicator = repo.save(
            Indicator(
                id=str(uuid.uuid4()),
                **serializer.validated_data,
            )
        )

        return Response(
            IndicatorSerializer(indicator).data,
            status=status.HTTP_201_CREATED,
        )
