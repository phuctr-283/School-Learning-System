from rest_framework import serializers


class CreateSemesterLessonPlanItemSerializer(
    serializers.Serializer
):

    semester_number = serializers.ChoiceField(
        choices=[
            "1",
            "2",
            "3",
        ]
    )

    total_lessons = serializers.IntegerField(
        min_value=1,
        max_value=100,
    )


class CreateSemesterLessonPlanSerializer(
    serializers.Serializer
):

    academic_year_id = serializers.CharField(
        required=True
    )

    semesters = (
        CreateSemesterLessonPlanItemSerializer(
            many=True,
            required=True,
            allow_empty=False,
        )
    )

