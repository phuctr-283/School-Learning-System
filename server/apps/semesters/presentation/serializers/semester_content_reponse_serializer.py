from rest_framework import serializers
class SemesterContentResponseSerializer(
    serializers.Serializer
):

    semester_id = serializers.CharField()

    name = serializers.CharField()

    semester_number = serializers.CharField()

    academic_year_id = serializers.CharField()

    academic_year_name = serializers.CharField()

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    status = serializers.CharField()