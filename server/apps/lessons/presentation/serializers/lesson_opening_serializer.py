from rest_framework import serializers


class LessonOpeningSerializer(
    serializers.Serializer
):

    lesson_opening_id = serializers.CharField()

    university_id = serializers.CharField()
    university_name = serializers.CharField()

    class_section_lesson_plan_id = (
        serializers.CharField()
    )

    lesson_id = serializers.CharField()
    lesson_number = serializers.IntegerField()
    lesson_name = serializers.CharField()

    status = serializers.CharField()

    opened_at = serializers.DateTimeField(
        allow_null=True,
    )

    closed_at = serializers.DateTimeField(
        allow_null=True,
    )

    created_at = serializers.DateTimeField()

    updated_at = serializers.DateTimeField()