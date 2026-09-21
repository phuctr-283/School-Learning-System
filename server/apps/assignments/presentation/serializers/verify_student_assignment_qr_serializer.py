from rest_framework import serializers


class VerifyStudentAssignmentQrSerializer(
    serializers.Serializer
):

    student_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    assignment_application_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    class_section_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    lesson_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )