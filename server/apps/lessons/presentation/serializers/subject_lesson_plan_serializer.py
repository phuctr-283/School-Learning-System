from rest_framework import serializers


class SubjectLessonPlanSerializer(
    serializers.Serializer
):

    subject_lesson_plan_id = serializers.CharField()

    university_id = serializers.CharField()

    semester_number = serializers.CharField()

    lesson_type = serializers.CharField()

    min_credits = serializers.IntegerField(
        allow_null=True,
    )

    max_credits = serializers.IntegerField(
        allow_null=True,
    )

    total_lessons = serializers.IntegerField()

    is_custom = serializers.BooleanField()