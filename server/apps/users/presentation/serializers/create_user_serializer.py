from rest_framework import serializers

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class CreateUserSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        max_length=100,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128,
        write_only=True,
    )

    account_level = serializers.ChoiceField(
        choices=[level.value for level in AccountLevel],
        required=True,
    )

    university_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=50,
    )

    def validate_username(
        self,
        value,
    ):

        value = value.strip().lower()

        if not value:

            raise serializers.ValidationError("Username không được để trống.")

        return value

    def validate_university_id(
        self,
        value,
    ):

        if value:

            return value.strip()

        return None
