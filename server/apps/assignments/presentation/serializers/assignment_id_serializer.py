from rest_framework import serializers


class AssignmentSerializer(
    serializers.Serializer
):
    assignment_id = serializers.CharField()

    class_section_id = serializers.CharField()

    lesson_id = serializers.CharField()

    lesson_number = serializers.IntegerField()

    title = serializers.CharField()

    description = serializers.CharField(
        allow_blank=True,
    )

    assignment_kind = serializers.CharField()

    exam_type = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )