from rest_framework import serializers

from apps.lessons.presentation.serializers.lesson_opening_serializer import (
    LessonOpeningSerializer,
)


class ClassSectionLessonPlanResponseSerializer(
    serializers.Serializer
):

    class_section_lesson_plan_id = (
        serializers.CharField()
    )

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    course_lesson_plan_id = serializers.CharField()

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

    is_custom = serializers.BooleanField()

    custom_total_lessons = serializers.IntegerField(
        allow_null=True,
        required=False,
    )

    effective_total_lessons = (
        serializers.IntegerField()
    )

    lesson_openings = LessonOpeningSerializer(
        many=True,
    )