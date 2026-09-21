from rest_framework import serializers


class CreateSemesterSerializer(
    serializers.Serializer
):

    academic_year_id = serializers.CharField(
        required=True
    )

    semester_number = serializers.ChoiceField(
        choices=[
            "1",
            "2",
            "3",
        ],
        required=True,
    )

    start_date = serializers.DateField(
        required=True,
        input_formats=[
            "%Y-%m-%d",
        ],
    )

    end_date = serializers.DateField(
        required=True,
        input_formats=[
            "%Y-%m-%d",
        ],
    )