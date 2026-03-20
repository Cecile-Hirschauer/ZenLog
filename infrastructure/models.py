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
    
    
class Indicator(models.Model):
    """A wellness metric that patients can track (e.g., mood, sleep).

    Maps to the domain entity domain.entities.indicator.Indicator.
    Managed by admins only. Patients select from active indicators.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20)
    min_value = models.FloatField()
    max_value = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wellness_indicator"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.unit})"
    
    
class WellnessEntry(models.Model):
    """A daily wellness measurement recorded by a patient.

    Maps to the domain entity domain.entities.wellness_entry.WellnessEntry.
    Enforces one entry per patient per indicator per day via unique constraint.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wellness_entries",
        limit_choices_to={"role": User.Role.PATIENT},
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.PROTECT,
        related_name="entries",
    )
    date = models.DateField()
    value = models.FloatField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wellness_entry"
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "indicator", "date"],
                name="unique_entry_per_patient_indicator_date",
            ),
        ]
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.patient_id} - {self.indicator.name} - {self.date}"
    
    
class Assignment(models.Model):
    """A coach-patient relationship with lifecycle management.

    Maps to the domain entity domain.entities.assignment.Assignment.
    Only admins can create or deactivate assignments.
    Active assignment grants the coach read-only access to patient data.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coach = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="coaching_assignments",
        limit_choices_to={"role": User.Role.COACH},
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_assignments",
        limit_choices_to={"role": User.Role.PATIENT},
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wellness_assignment"
        constraints = [
            models.UniqueConstraint(
                fields=["coach", "patient"],
                condition=models.Q(is_active=True),
                name="unique_active_assignment_per_coach_patient",
            ),
        ]

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"Coach {self.coach_id} → Patient {self.patient_id} ({status})"
    
