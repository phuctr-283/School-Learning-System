from rest_framework import serializers


class TeacherClassSectionSerializer(
    serializers.Serializer
):

    university_id = serializers.CharField()

    department_id = serializers.CharField()

    class_section_id = serializers.CharField()

    academic_year_id = serializers.CharField()

    academic_year_name = serializers.CharField()

    semester_id = serializers.CharField()

    semester_name = serializers.CharField()

    semester_number = serializers.CharField()

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()

    group_number = serializers.IntegerField()

    status = serializers.CharField()