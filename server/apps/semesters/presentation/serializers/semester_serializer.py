from rest_framework import serializers


class SemesterSerializer(serializers.Serializer):

    semester_id = serializers.CharField()
    name = serializers.CharField()
    semester_number = serializers.CharField()
    academic_year_id = serializers.CharField()
    academic_year_name = serializers.CharField()
    university_id = serializers.CharField()
    university_name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField()
class ActivePlannedSemesterQuerySerializer(
    serializers.Serializer
):

    university_id = serializers.CharField(
        required=True,
        max_length=50,
    )