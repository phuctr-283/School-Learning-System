from rest_framework import serializers


class AssignmentContentSerializer(
    serializers.Serializer
):

    assignment_id = serializers.CharField()

    university_id = serializers.CharField()

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()

    teacher_id = serializers.CharField()

    title = serializers.CharField()

    description = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
    )

    assignment_type = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    duration_minutes = serializers.IntegerField()

    status = serializers.CharField()

    is_active = serializers.BooleanField()

    created_at = serializers.DateTimeField(
        allow_null=True,
    )

    updated_at = serializers.DateTimeField(
        allow_null=True,
    )