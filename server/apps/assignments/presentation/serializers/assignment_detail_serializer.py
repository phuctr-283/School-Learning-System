from rest_framework import serializers


class AssignmentQuestionDetailSerializer(serializers.Serializer):
    question_type = serializers.CharField()

    question = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    content = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    answer = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    def to_representation(self, instance):

        question_type = str(
            getattr(
                instance,
                "question_type",
                "",
            )
            or ""
        ).strip()

        question = (
            getattr(
                instance,
                "question",
                "",
            )
            or ""
        )

        content = (
            getattr(
                instance,
                "content",
                "",
            )
            or ""
        )

        score = getattr(
            instance,
            "score",
            None,
        )

        options = (
            getattr(
                instance,
                "options",
                None,
            )
            or []
        )

        answer_object = getattr(
            instance,
            "answer",
            None,
        )

        # ==================================================
        # MULTIPLE CHOICE
        # ==================================================

        if question_type == "multiple_choice":

            correct_option_ids = set(
                str(option_id)
                for option_id in (
                    getattr(
                        answer_object,
                        "correct_option_ids",
                        None,
                    )
                    or []
                )
            )

            sorted_options = sorted(
                options,
                key=lambda option: (
                    getattr(
                        option,
                        "order",
                        0,
                    )
                    or 0
                ),
            )

            answer_lines = []

            for index, option in enumerate(sorted_options):

                option_id = str(
                    getattr(
                        option,
                        "option_id",
                        "",
                    )
                    or ""
                )

                option_content = str(
                    getattr(
                        option,
                        "content",
                        "",
                    )
                    or ""
                ).strip()

                letter = chr(ord("A") + index)

                is_correct = option_id in correct_option_ids

                prefix = "*" if is_correct else ""

                answer_lines.append(f"{prefix}{letter}. {option_content}")

            answer = "\n".join(answer_lines)

        # ==================================================
        # ORDERING
        # ==================================================

        elif question_type == "ordering":

            sorted_options = sorted(
                options,
                key=lambda option: (
                    getattr(
                        option,
                        "order",
                        0,
                    )
                    or 0
                ),
            )

            answer_lines = []

            for option in sorted_options:

                option_content = str(
                    getattr(
                        option,
                        "content",
                        "",
                    )
                    or ""
                ).strip()

                if option_content:
                    answer_lines.append(option_content)

            answer = "\n".join(answer_lines)

        # ==================================================
        # DRAG AND DROP
        # ==================================================

        elif question_type == "drag_and_drop":

            correct_answers = (
                getattr(
                    answer_object,
                    "correct_answers",
                    None,
                )
                or []
            )

            # Map option_id -> content
            option_map = {
                str(
                    getattr(
                        option,
                        "option_id",
                        "",
                    )
                    or ""
                ): str(
                    getattr(
                        option,
                        "content",
                        "",
                    )
                    or ""
                ).strip()
                for option in options
            }

            answer_lines = []

            for correct_answer in correct_answers:

                value = str(correct_answer or "").strip()

                if not value:
                    continue

                # Nếu correct_answers lưu option_id
                value = option_map.get(
                    value,
                    value,
                )

                answer_lines.append(f"*{value}")

            answer = "\n".join(answer_lines)

        # ==================================================
        # FALLBACK
        # ==================================================

        else:

            answer = ""

            if answer_object is not None:

                answer = str(answer_object)

        return {
            "question_type": question_type,
            "question": question,
            "content": content,
            "answer": answer,
            "score": score,
        }


class AssignmentDetailSerializer(serializers.Serializer):

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

    questions = AssignmentQuestionDetailSerializer(many=True)

    total_score = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    duration_minutes = serializers.IntegerField()

    status = serializers.CharField()

    is_active = serializers.BooleanField()

    created_at = serializers.DateTimeField(allow_null=True)

    updated_at = serializers.DateTimeField(allow_null=True)
