from rest_framework import serializers


class ClassSectionSerializer(
    serializers.Serializer
):

    class_section_id = serializers.CharField()

    subject_id = serializers.CharField()
    subject_name = serializers.CharField()

    group_number = serializers.IntegerField()

    teacher_id = serializers.CharField()
    teacher_name = serializers.CharField()

    semester_id = serializers.CharField()
    semester_name = serializers.CharField()
    semester_number = serializers.CharField()

    academic_year_id = serializers.CharField()
    academic_year_name = serializers.CharField()

    university_id = serializers.CharField()
    university_name = serializers.CharField()

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    status = serializers.CharField()