from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ThrottledTokenObtainPairView(TokenObtainPairView):
    """Token endpoint with auth throttle scope."""

    throttle_scope = "auth"


class ThrottledTokenRefreshView(TokenRefreshView):
    """Token refresh endpoint with auth throttle scope."""

    throttle_scope = "auth"
