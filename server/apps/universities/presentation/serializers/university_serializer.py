from rest_framework import serializers


class UniversitySerializer(serializers.Serializer):

    university_id = serializers.CharField()

    name = serializers.CharField()

    domain = serializers.CharField()

    email = serializers.EmailField()

    phone = serializers.CharField()

    is_active = serializers.BooleanField()

    updated_at = serializers.DateTimeField()
