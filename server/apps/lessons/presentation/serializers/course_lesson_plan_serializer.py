from rest_framework import serializers


class CourseLessonPlanResponseSerializer(
    serializers.Serializer
):

    course_lesson_plan_id = serializers.CharField()

    university_id = serializers.CharField()
    university_name = serializers.CharField()

    subject_id = serializers.CharField()
    subject_name = serializers.CharField()

    semester_id = serializers.CharField()
    semester_name = serializers.CharField()
    semester_number = serializers.CharField()

    academic_year_id = serializers.CharField()
    academic_year_name = serializers.CharField()

    total_lessons = serializers.IntegerField()