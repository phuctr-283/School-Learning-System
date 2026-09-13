from rest_framework import serializers


class SubjectLessonPlanRuleSerializer(
    serializers.Serializer
):

    lesson_type = serializers.ChoiceField(
        choices=[
            "theory",
            "practice",
        ]
    )

    min_credits = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0,
    )

    max_credits = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0,
    )

    total_lessons = serializers.IntegerField(
        required=True,
        min_value=1,
    )


class CreateSubjectLessonPlanSerializer(
    serializers.Serializer
):

    semester_number = serializers.ChoiceField(
        choices=[
            "1",
            "2",
            "3",
        ]
    )

    rules = SubjectLessonPlanRuleSerializer(
        many=True,
        allow_empty=False,
    )