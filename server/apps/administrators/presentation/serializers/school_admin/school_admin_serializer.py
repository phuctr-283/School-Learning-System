from rest_framework import serializers


class SchoolAdminSerializer(serializers.Serializer):

    school_admin_id = serializers.CharField()

    full_name = serializers.CharField()

    gender = serializers.CharField(
        allow_null=True,
        required=False,
    )

    email = serializers.EmailField()

    phone = serializers.CharField(
        allow_null=True,
        required=False,
    )

    university_id = serializers.CharField(
        allow_null=True,
        required=False,
    )

    university_name = serializers.CharField(
        allow_null=True,
        required=False,
    )

    status = serializers.CharField()