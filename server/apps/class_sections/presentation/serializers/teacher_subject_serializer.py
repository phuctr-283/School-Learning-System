from rest_framework import serializers


class TeacherSubjectSerializer(
    serializers.Serializer
):

    university_id = serializers.CharField()

    department_id = serializers.CharField()

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()