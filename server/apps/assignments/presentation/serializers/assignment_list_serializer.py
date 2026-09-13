from rest_framework import serializers


class AssignmentListSerializer(
    serializers.Serializer,
):

    assignment_id = serializers.CharField()
    title = serializers.CharField()

    description = serializers.CharField(
        allow_null=True,
        required=False,
    )

    university_id = serializers.CharField()
    department_id = serializers.CharField()
    subject_id = serializers.CharField()
    teacher_id = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    assignment_type = serializers.CharField()
    status = serializers.CharField()
    is_active = serializers.BooleanField()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()