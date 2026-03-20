from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from infrastructure.serializers.auth import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — Create a new user account.

    Public endpoint (no authentication required).
    Password is hashed before storage, never returned in response.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
