from rest_framework import serializers


class StudentSerializer(serializers.Serializer):

    student_id = serializers.CharField()

    full_name = serializers.CharField()

    gender = serializers.CharField()

    student_class = serializers.CharField()

    department_id = serializers.CharField()

    department_name = serializers.CharField()

    cohort_id = serializers.CharField()

    status = serializers.CharField()

    university_id = serializers.CharField()

    university_name = serializers.CharField()

    date_of_birth = serializers.DateField(
        allow_null=True,
    )

    email = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )

    phone = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
