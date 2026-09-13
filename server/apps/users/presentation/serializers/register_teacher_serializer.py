from rest_framework import serializers
class RegisterTeacherSerializer(
    serializers.Serializer
):

    username = serializers.EmailField(
        required=True,
        max_length=100,
    )

    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128,
        write_only=True,
    )

    full_name = serializers.CharField(
        required=True,
        max_length=100,
        trim_whitespace=True,
    )

    department_id = serializers.CharField(
        required=True,
        max_length=50,
    )

    def validate_username(
        self,
        value,
    ):

        return value.strip().lower()

    def validate_full_name(
        self,
        value,
    ):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Họ và tên không được để trống."
            )

        return value

    def validate_department_id(
        self,
        value,
    ):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Vui lòng chọn khoa."
            )

        return value