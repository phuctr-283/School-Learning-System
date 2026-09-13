from rest_framework import serializers


class RegisterTeacherSerializer(serializers.Serializer):

    full_name = serializers.CharField(
        required=True,
        max_length=255,
    )

    university_id = serializers.CharField(
        required=True,
        max_length=50,
    )

    department_id = serializers.CharField(
        required=True,
        max_length=20,
    )

    email = serializers.EmailField(
        required=True,
        max_length=255,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=20,
    )

    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=20,
    )

    def validate_full_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Họ và tên không được để trống")

        return value

    def validate_university_id(self, value):

        return value.strip().upper()

    def validate_department_id(self, value):

        return value.strip().upper()

    def validate_email(self, value):

        return value.strip().lower()

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Mật khẩu nhập lại không khớp"}
            )

        return attrs
