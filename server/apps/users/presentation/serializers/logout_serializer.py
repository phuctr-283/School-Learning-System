from rest_framework import serializers


class LogoutSerializer(
    serializers.Serializer
):

    refresh_token = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate_refresh_token(
        self,
        value,
    ):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Refresh token không được để trống."
            )

        return value