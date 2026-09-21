from rest_framework import serializers

class AssignmentQuestionInputSerializer(
    serializers.Serializer,
):
    question_type = serializers.ChoiceField(
        choices=[
            "multiple_choice",
            "ordering",
            "drag_and_drop",
        ],
    )

    question = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    content = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    answer = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    score = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=5,
        decimal_places=2,
        min_value="0.01",
        max_value="10.00",
    )