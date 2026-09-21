from rest_framework import serializers


class AssignmentApplicationLessonSerializer(
    serializers.Serializer
):

    assignment_application_id = serializers.CharField()

    assignment_id = serializers.CharField()

    class_section_id = serializers.CharField()

    lesson_id = serializers.CharField()

    title = serializers.CharField()

    is_active = serializers.BooleanField()