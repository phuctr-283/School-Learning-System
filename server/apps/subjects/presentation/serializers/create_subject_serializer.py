from rest_framework import serializers


class CreateSubjectSerializer(serializers.Serializer):

    subject_id = serializers.CharField(
        max_length=30,
    )

    name = serializers.CharField(
        max_length=255,
    )

    department_id = serializers.CharField(
        max_length=30,
    )

    subject_types = serializers.ChoiceField(
        choices=[
            "Theory",
            "Practice",
        ],
    )

    credits = serializers.IntegerField(
        min_value=1,
    )

    process_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )

    midterm_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )

    final_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )

    def validate(self, attrs):

        total = (
            attrs["process_percent"] + attrs["midterm_percent"] + attrs["final_percent"]
        )

        if total != 100:
            raise serializers.ValidationError("Tổng tỷ lệ điểm phải bằng 100%.")

        return attrs
