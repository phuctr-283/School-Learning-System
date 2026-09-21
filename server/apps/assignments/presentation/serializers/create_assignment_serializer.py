from rest_framework import serializers
from apps.assignments.presentation.serializers.assignment_question_input_serializer import AssignmentQuestionInputSerializer
class CreateAssignmentSerializer(
    serializers.Serializer,
):
    title = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    subject_id = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    assignment_type = serializers.ChoiceField(
        choices=[
            "practice",
            "homework",
            "quiz",
        ],
    )

    duration_minutes = serializers.IntegerField(
        min_value=1,
        max_value=600,
    )

    questions = AssignmentQuestionInputSerializer(
        many=True,
        allow_empty=False,
    )