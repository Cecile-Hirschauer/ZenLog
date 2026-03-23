from django.urls import path
from rest_framework.routers import DefaultRouter

from infrastructure.views.auth import RegisterView
from infrastructure.views.coaching import (
    CoachingPatientEntriesView,
    CoachingPatientsView,
)
from infrastructure.views.indicators import IndicatorViewSet
from infrastructure.views.token import (
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
)
from infrastructure.views.trends import TrendView
from infrastructure.views.wellness import WellnessEntryViewSet

router = DefaultRouter()
router.register(r"wellness/entries", WellnessEntryViewSet, basename="wellness-entry")
router.register(r"wellness/indicators", IndicatorViewSet, basename="wellness-indicator")

urlpatterns = [
    # Auth endpoints
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/token/", ThrottledTokenObtainPairView.as_view(), name="auth-token"),
    path(
        "auth/token/refresh/",
        ThrottledTokenRefreshView.as_view(),
        name="auth-token-refresh",
    ),
    # Trends (not a ViewSet, standalone APIView)
    path("wellness/trends/", TrendView.as_view(), name="wellness-trends"),
    # Coaching endpoints
    path(
        "coaching/patients/", CoachingPatientsView.as_view(), name="coaching-patients"
    ),
    path(
        "coaching/patients/<uuid:patient_id>/entries/",
        CoachingPatientEntriesView.as_view(),
        name="coaching-patient-entries",
    ),
] + router.urls
