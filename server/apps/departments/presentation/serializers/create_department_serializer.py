from rest_framework import serializers


class CreateDepartmentSerializer(
    serializers.Serializer,
):

    department_id = serializers.CharField(
        required=True,
        max_length=20,
    )

    department_number = serializers.CharField(
        required=True,
        max_length=10,
    )

    name = serializers.CharField(
        required=True,
        max_length=255,
    )

    head_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
