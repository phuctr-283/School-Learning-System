from rest_framework import serializers


class CreateAcademicYearSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=20,
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

    def validate_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Tên năm học không được để trống"
            )

        return value