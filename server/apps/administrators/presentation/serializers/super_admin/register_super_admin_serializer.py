from rest_framework import serializers


class RegisterSuperAdminSerializer(
    serializers.Serializer
):

    full_name = serializers.CharField(
        max_length=100,
        required=True,
    )

    username = serializers.EmailField(
        max_length=100,
        required=True,
    )

    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
    )