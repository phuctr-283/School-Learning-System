from rest_framework import serializers


class GetActiveDepartmentsByUniversitySerializer(
    serializers.Serializer
):

    department_id = serializers.CharField()

    department_number = serializers.CharField()

    name = serializers.CharField()