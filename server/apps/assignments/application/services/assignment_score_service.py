from decimal import (
    Decimal,
    ROUND_HALF_UP,
)


class AssignmentScoreService:

    TOTAL_SCORE = Decimal("10.00")
    MIN_SCORE = Decimal("0.01")

    @classmethod
    def assign_scores_if_missing(
        cls,
        questions,
    ):
        if not questions:
            raise ValueError("Danh sách câu hỏi không được để trống.")

        explicit_questions = []
        missing_questions = []

        for question in questions:
            score = question.score

            if score is None or score <= Decimal("0.00"):
                missing_questions.append(
                    question,
                )
            else:
                explicit_questions.append(
                    question,
                )

        explicit_total = sum(
            (q.score for q in explicit_questions),
            Decimal("0.00"),
        )

        if explicit_total > cls.TOTAL_SCORE:
            raise ValueError("Tổng điểm các câu hỏi vượt quá 10.")

        if not missing_questions:
            if explicit_total != cls.TOTAL_SCORE:
                raise ValueError("Tổng điểm các câu hỏi phải bằng 10.")

            return questions

        remaining = cls.TOTAL_SCORE - explicit_total

        if remaining < cls.MIN_SCORE * len(missing_questions):
            raise ValueError(
                "Không đủ điểm để phân bổ " "cho các câu hỏi chưa nhập điểm."
            )

        base_score = (
            remaining
            / Decimal(
                str(
                    len(
                        missing_questions,
                    )
                )
            )
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        assigned_total = base_score * len(missing_questions)

        remainder = remaining - assigned_total

        for index, question in enumerate(
            missing_questions,
        ):
            question.score = base_score

            if index == len(missing_questions) - 1:
                question.score += remainder

        return questions
