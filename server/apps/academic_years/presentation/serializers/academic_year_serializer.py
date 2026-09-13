from rest_framework import serializers


class AcademicYearSerializer(serializers.Serializer):

    academic_year_id = serializers.CharField()

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    name = serializers.CharField()

    start_date = serializers.DateField()

    end_date = serializers.DateField()

    status = serializers.CharField()
