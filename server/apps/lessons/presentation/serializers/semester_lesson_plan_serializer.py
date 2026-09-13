from rest_framework import serializers
class SemesterLessonPlanSerializer(
    serializers.Serializer
):

    semester_lesson_plan_id = serializers.CharField()

    university_id = serializers.CharField()

    semester_id = serializers.CharField()

    academic_year_id = serializers.CharField()

    academic_year_name = serializers.CharField()

    semester_number = serializers.CharField()

    total_lessons = serializers.IntegerField()