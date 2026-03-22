from rest_framework import serializers


class CreateEntrySerializer(serializers.Serializer):
    """Input serializer for creating a wellness entry.

    patient_id is NOT in the input — it comes from request.user.
    """

    indicator_id = serializers.UUIDField()
    date = serializers.DateField()
    value = serializers.FloatField()
    note = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateEntrySerializer(serializers.Serializer):
    """Input serializer for updating a wellness entry."""

    value = serializers.FloatField(required=False)
    note = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class EntrySerializer(serializers.Serializer):
    """Output serializer for a wellness entry."""

    id = serializers.CharField()
    patient_id = serializers.CharField()
    indicator_id = serializers.CharField()
    date = serializers.DateField()
    value = serializers.FloatField()
    note = serializers.CharField(allow_null=True)


class TrendSerializer(serializers.Serializer):
    """Output serializer for a trend."""

    patient_id = serializers.CharField()
    indicator_id = serializers.CharField()
    period_days = serializers.IntegerField()
    average = serializers.FloatField(allow_null=True)
    entry_count = serializers.IntegerField()


class IndicatorSerializer(serializers.Serializer):
    """Output serializer for an indicator."""

    id = serializers.CharField()
    name = serializers.CharField()
    unit = serializers.CharField()
    min_value = serializers.FloatField()
    max_value = serializers.FloatField()
    is_active = serializers.BooleanField()


class CreateIndicatorSerializer(serializers.Serializer):
    """Input serializer for creating an indicator (admin only)."""

    name = serializers.CharField(max_length=100)
    unit = serializers.CharField(max_length=20)
    min_value = serializers.FloatField()
    max_value = serializers.FloatField()