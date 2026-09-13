from rest_framework import serializers


class SubjectSerializer(serializers.Serializer):

    subject_id = serializers.CharField()

    name = serializers.CharField()

    university_id = serializers.CharField()
    university_name = serializers.CharField()

    department_id = serializers.CharField()
    department_name = serializers.CharField()

    subject_types = serializers.CharField()

    credits = serializers.IntegerField()

    process_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    midterm_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    final_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    status = serializers.CharField()