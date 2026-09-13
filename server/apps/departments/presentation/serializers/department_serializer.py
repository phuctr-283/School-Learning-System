from rest_framework import serializers


class DepartmentSerializer(
    serializers.Serializer
):

    department_id = serializers.CharField()

    department_number = serializers.CharField()

    name = serializers.CharField()

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    head_id = serializers.CharField(
        allow_null=True,
    )

    head_name = serializers.CharField(
        allow_null=True,
    )

    is_active = serializers.BooleanField()