from rest_framework import serializers


class AssignmentHistoryOptionSerializer(
    serializers.Serializer,
):

    option_id = serializers.CharField()
    content = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    is_correct = serializers.BooleanField()
    is_selected = serializers.BooleanField()
    is_selected_correct = serializers.BooleanField()
    is_selected_wrong = serializers.BooleanField()


class AssignmentHistoryQuestionSerializer(
    serializers.Serializer,
):
    question_id = serializers.CharField()
    question = serializers.CharField()
    content = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    question_type = serializers.CharField()

    score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    earned_score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    user_answer = serializers.JSONField(
        allow_null=True,
    )

    correct_answer = serializers.JSONField(
        allow_null=True,
    )

    correct = serializers.BooleanField()

    options = AssignmentHistoryOptionSerializer(
        many=True,
    )
    correct_options = AssignmentHistoryOptionSerializer(
        many=True,
    )

    wrong_options = AssignmentHistoryOptionSerializer(
        many=True,
    )

class AssignmentHistorySerializer(
    serializers.Serializer,
):
    attempt_id = serializers.CharField()

    assignment_application_id = serializers.CharField()
    assignment_id = serializers.CharField()
    lesson_id = serializers.CharField()

    title = serializers.CharField()
    subject_name = serializers.CharField()
    assignment_type = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    percentage = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    answered_count = serializers.IntegerField()
    correct_count = serializers.IntegerField()

    started_at = serializers.DateTimeField()
    submitted_at = serializers.DateTimeField(
        allow_null=True,
    )

    questions = AssignmentHistoryQuestionSerializer(
        many=True,
    )
