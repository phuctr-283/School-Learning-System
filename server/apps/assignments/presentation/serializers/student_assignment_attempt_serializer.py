from rest_framework import serializers


class StudentAssignmentAttemptSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    full_name = serializers.CharField(allow_blank=True)

    status = serializers.CharField()
    status_label = serializers.CharField()

    score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        allow_null=True,
    )

    total_score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        allow_null=True,
    )

    attempt_id = serializers.CharField(allow_null=True)


class StudentAssignmentAttemptsSerializer(serializers.Serializer):
    assignment_application_id = serializers.CharField()
    class_section_id = serializers.CharField()
    lesson_id = serializers.CharField()

    students = StudentAssignmentAttemptSerializer(many=True)
