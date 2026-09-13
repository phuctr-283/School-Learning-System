from rest_framework import serializers


class TeacherSerializer(
    serializers.Serializer,
):

    teacher_id = serializers.CharField()

    full_name = serializers.CharField()

    gender = serializers.CharField(
        allow_null=True,
        required=False,
    )

    date_of_birth = serializers.DateField(
        allow_null=True,
        required=False,
    )

    email = serializers.EmailField(
        allow_null=True,
        required=False,
    )

    phone = serializers.CharField(
        allow_null=True,
        required=False,
    )

    department_id = serializers.CharField()

    department_name = serializers.CharField()

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    status = serializers.CharField()
