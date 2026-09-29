from rest_framework import serializers


class AssignmentQuestionDetailSerializer(
    serializers.Serializer
):
    question_type = serializers.CharField()

    question = serializers.CharField()

    content = serializers.CharField(
        allow_blank=True
    )

    answer = serializers.CharField(
        allow_blank=True
    )

    score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        allow_null=True,
    )


class AssignmentDetailSerializer(
    serializers.Serializer
):

    assignment_id = serializers.CharField()

    university_id = serializers.CharField()

    department_id = serializers.CharField()

    subject_id = serializers.CharField()

    teacher_id = serializers.CharField()

    title = serializers.CharField()

    description = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )

    assignment_type = serializers.CharField()

    questions = (
        AssignmentQuestionDetailSerializer(
            many=True
        )
    )

    total_score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    duration_minutes = serializers.IntegerField()

    status = serializers.CharField()

    is_active = serializers.BooleanField()

    created_at = serializers.DateTimeField(
        allow_null=True
    )

    updated_at = serializers.DateTimeField(
        allow_null=True
    )