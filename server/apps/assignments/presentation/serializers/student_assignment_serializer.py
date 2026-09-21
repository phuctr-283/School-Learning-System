from rest_framework import serializers


class StudentAssignmentOptionSerializer(
    serializers.Serializer
):

    option_id = serializers.CharField()

    content = serializers.CharField()

    order = serializers.IntegerField()


class StudentAssignmentQuestionSerializer(
    serializers.Serializer
):

    question_id = serializers.CharField()
    question = serializers.CharField()
    content = serializers.CharField()

    question_type = serializers.CharField()

    score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    order = serializers.IntegerField()

    shuffle_options = serializers.BooleanField()

    blank_count = serializers.IntegerField()

    options = StudentAssignmentOptionSerializer(
        many=True
    )


class StudentAssignmentReviewSerializer(
    serializers.Serializer
):

    question_id = serializers.CharField()

    question_type = serializers.CharField()

    user_answer = serializers.JSONField(
        allow_null=True
    )

    correct = serializers.BooleanField()

    score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    correct_answer = serializers.JSONField(
        allow_null=True
    )


class StudentAssignmentResultSerializer(
    serializers.Serializer
):

    score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    total_score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    percentage = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    answered_count = serializers.IntegerField()

    correct_count = serializers.IntegerField()

    submitted_at = serializers.DateTimeField(
        allow_null = True
    )

    review = StudentAssignmentReviewSerializer(
        many=True
    )


class StudentAssignmentSerializer(
    serializers.Serializer
):

    assignment_application_id = serializers.CharField()

    assignment_id = serializers.CharField()

    lesson_id = serializers.CharField()

    title = serializers.CharField()

    description = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()

    assignment_type = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    duration_minutes = serializers.IntegerField()

    max_attempts = serializers.IntegerField()

    open_at = serializers.DateTimeField(
        allow_null=True
    )

    due_at = serializers.DateTimeField(
        allow_null=True
    )

    attempt_id = serializers.CharField()

    attempt_status = serializers.CharField()

    remaining_seconds = serializers.IntegerField()

    saved_answers = serializers.JSONField()

    questions = StudentAssignmentQuestionSerializer(
        many=True
    )

    result = StudentAssignmentResultSerializer(
        allow_null=True
    )