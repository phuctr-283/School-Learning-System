from rest_framework import serializers


class StudentClassSectionSerializer(
    serializers.Serializer
):
    class_section_id = serializers.CharField()

    academic_year_id = serializers.CharField()

    semester_id = serializers.CharField()

    subject_id = serializers.CharField()

    group_number = serializers.IntegerField()

    subject_name = serializers.CharField()

    teacher_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )