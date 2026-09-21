from rest_framework import serializers


class StudentLessonSerializer(
    serializers.Serializer
):

    lesson_id = serializers.CharField()

    lesson_number = serializers.IntegerField()

    lesson_name = serializers.CharField()

    status = serializers.ChoiceField(
        choices=[
            "locked",
            "open",
            "closed",
        ]
    )

    opened_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )

    closed_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )


class StudentClassSectionLessonPlanSerializer(
    serializers.Serializer
):

    class_section_lesson_plan_id = (
        serializers.CharField()
    )

    class_section_id = serializers.CharField()

    group_number = serializers.IntegerField()

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()

    semester_id = serializers.CharField()

    semester_name = serializers.CharField()

    semester_number = serializers.CharField()

    academic_year_id = serializers.CharField()

    academic_year_name = serializers.CharField()

    total_lessons = serializers.IntegerField()

    lesson_openings = StudentLessonSerializer(
        many=True
    )