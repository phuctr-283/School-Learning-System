from rest_framework import serializers


class UniversitySerializer(serializers.Serializer):

    university_id = serializers.CharField()

    name = serializers.CharField()