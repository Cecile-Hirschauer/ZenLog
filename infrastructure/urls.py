from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from infrastructure.views.auth import RegisterView
from infrastructure.views.indicators import IndicatorViewSet
from infrastructure.views.trends import TrendView
from infrastructure.views.wellness import WellnessEntryViewSet

router = DefaultRouter()
router.register(r"wellness/entries", WellnessEntryViewSet, basename="wellness-entry")
router.register(r"wellness/indicators", IndicatorViewSet, basename="wellness-indicator")

urlpatterns = [
    # Auth endpoints
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="auth-token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    # Trends (not a ViewSet, standalone APIView)
    path("wellness/trends/", TrendView.as_view(), name="wellness-trends"),
] + router.urls
