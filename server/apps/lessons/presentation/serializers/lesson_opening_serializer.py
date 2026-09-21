from rest_framework import serializers


class LessonOpeningSerializer(
    serializers.Serializer
):

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