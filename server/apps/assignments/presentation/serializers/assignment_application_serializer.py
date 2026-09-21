from rest_framework import serializers


class AssignmentApplicationSerializer(
    serializers.Serializer
):

    assignment_application_id = (
        serializers.CharField()
    )

    assignment_id = serializers.CharField()

    class_section_ids = serializers.ListField(
        child=serializers.CharField()
    )

    lesson_id = serializers.CharField()

    status = serializers.CharField()

    open_at = serializers.DateTimeField(
        allow_null=True,
    )

    due_at = serializers.DateTimeField(
        allow_null=True,
    )

    max_attempts = serializers.IntegerField()