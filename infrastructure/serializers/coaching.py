from rest_framework import serializers


class PatientListSerializer(serializers.Serializer):
    """Response: list of patient IDs assigned to a coach."""

    patients = serializers.ListField(child=serializers.CharField())


class PatientEntrySerializer(serializers.Serializer):
    """Read-only wellness entry for coach view."""

    id = serializers.CharField()
    patient_id = serializers.CharField()
    indicator_id = serializers.CharField()
    date = serializers.DateField()
    value = serializers.FloatField()
    note = serializers.CharField(allow_null=True)
