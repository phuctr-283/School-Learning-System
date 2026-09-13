from rest_framework import serializers


class CreateLessonSerializer(
    serializers.Serializer,
):

    create_mode = serializers.ChoiceField(
        choices=[
            "single",
            "multiple",
        ],
    )

    lesson_number = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
    )

    lesson_number_start = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
    )

    lesson_number_end = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
    )