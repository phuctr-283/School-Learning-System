from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        max_length=100,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        required=True,
        max_length=128,
        write_only=True,
        style={"input_type": "password"},
    )

    def validate_username(
        self,
        value,
    ):

        value = value.strip().lower()

        if not value:

            raise serializers.ValidationError("Username không được để trống.")

        return value
