from decimal import Decimal

from rest_framework import serializers


class CreateAssignmentQuestionSerializer(
    serializers.Serializer
):

    question_type = serializers.ChoiceField(
        choices=[
            "multiple_choice",
            "ordering",
            "drag_and_drop",
        ]
    )

    content = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    options = serializers.ListField(
        child=serializers.CharField(
            allow_blank=False,
        ),
        required=True,
        allow_empty=False,
    )

    score = serializers.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0.01"),
        max_value=Decimal("10.00"),
    )


class CreateAssignmentSerializer(
    serializers.Serializer
):

    title = serializers.CharField(
        required=True,
        max_length=255,
        allow_blank=False,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    subject_id = serializers.CharField(
        required=True,
        max_length=50,
    )

    assignment_type = serializers.ChoiceField(
        choices=[
            "practice",
            "homework",
            "quiz",
        ],
        required=False,
        default="practice",
    )

    questions = CreateAssignmentQuestionSerializer(
        many=True,
        required=True,
        allow_empty=False,
    )