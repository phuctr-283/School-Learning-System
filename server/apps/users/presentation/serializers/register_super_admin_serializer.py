from rest_framework import serializers

class RegisterSuperAdminSerializer(
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

    def validate_username(
        self,
        value,
    ):

        value = value.strip().lower()

        if not value.endswith(
            "@admin.vn"
        ):
            raise serializers.ValidationError(
                "Super Admin phải sử dụng email @admin.vn."
            )

        return value