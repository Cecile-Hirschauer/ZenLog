"""Django app configuration for the infrastructure layer."""

from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
    """Django application config for the infrastructure app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "infrastructure"
