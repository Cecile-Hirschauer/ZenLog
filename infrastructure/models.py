import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with UUID primary key and role field.

    Extends Django's AbstractUser to add a role-based access control field.
    The role determines what the user can do in the system:
    - patient: can create and view their own wellness entries
    - coach: can view assigned patients' entries (read-only)
    - admin: can manage indicators, assignments and users
    """

    class Role(models.TextChoices):
        PATIENT = "patient", "Patient"
        COACH = "coach", "Coach"
        ADMIN = "admin", "Administrateur"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PATIENT,
        help_text="Role determining user permissions in the system.",
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "identity_user"
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

    def __str__(self):
        return f"{self.email} ({self.role})"
