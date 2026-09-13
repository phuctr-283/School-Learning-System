from rest_framework import serializers


class AssignmentContentSerializer(
    serializers.Serializer,
):

    assignment_id = serializers.CharField()
    title = serializers.CharField()

    description = serializers.CharField(
        allow_null=True,
        required=False,
    )

    university_id = serializers.CharField()
    department_id = serializers.CharField()
    subject_id = serializers.CharField()
    teacher_id = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    assignment_type = serializers.CharField()
    status = serializers.CharField()
    is_active = serializers.BooleanField()

    questions = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_questions(
        self,
        obj,
    ):

        return [
            {
                "question_id": question.question_id,
                "content": question.content,
                "question_type": question.question_type,
                "score": str(question.score),
                "order": question.order,
                "shuffle_options": (question.shuffle_options),
                "blank_count": question.blank_count,
                "options": [
                    {
                        "option_id": option.option_id,
                        "content": option.content,
                        "order": option.order,
                    }
                    for option in question.options
                ],
                "answer": (
                    {
                        "correct_option_ids": (question.answer.correct_option_ids),
                        "correct_order_option_ids": (
                            question.answer.correct_order_option_ids
                        ),
                        "correct_answers": (question.answer.correct_answers),
                    }
                    if question.answer
                    else None
                ),
                "test_cases": [
                    {
                        "test_case_id": (test_case.test_case_id),
                        "input": test_case.input,
                        "expected_output": (test_case.expected_output),
                        "order": test_case.order,
                        "is_hidden": test_case.is_hidden,
                    }
                    for test_case in question.test_cases
                ],
            }
            for question in obj.questions
        ]
