from rest_framework import serializers


class CreateUniversitySerializer(
    serializers.Serializer
):

    university_id = serializers.CharField(
        max_length=50,
        required=True,
    )

    name = serializers.CharField(
        max_length=200,
        required=True,
    )

    domain = serializers.CharField(
        max_length=100,
        required=True,
    )

    email = serializers.EmailField(
        max_length=150,
        required=True,
    )

    phone = serializers.CharField(
        max_length=20,
        required=True,
    )

