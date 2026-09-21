import re

from decimal import Decimal

from apps.assessment.domain.entities.assessment_question_entity import (
    AssessmentQuestion,
)

from apps.assessment.domain.entities.assessment_question_option_entity import (
    AssessmentQuestionOption,
)

from apps.assessment.domain.entities.assessment_question_answer_entity import (
    AssessmentQuestionAnswer,
)

from apps.assessment.application.services.question_input_mapper import (
    QuestionInputMapper,
)

from apps.assignments.application.services.assignment_score_service import (
    AssignmentScoreService,
)


class QuestionParserService:

    OPTION_PREFIX_PATTERN = re.compile(r"^\s*([A-Da-d])(?:[\.\)])\s*(.*)$")

    @classmethod
    def parse_questions(
        cls,
        raw_questions: list[dict],
    ) -> list[AssessmentQuestion]:

        normalized = QuestionInputMapper.to_parser_format(
            raw_questions,
        )

        if not normalized:
            raise ValueError("Danh sách câu hỏi không được để trống.")

        parsed = []

        for order, raw in enumerate(
            normalized,
            start=1,
        ):
            parsed.append(
                cls.parse_question(
                    raw,
                    order,
                )
            )

        return AssignmentScoreService.assign_scores_if_missing(
            parsed,
        )

    @classmethod
    def parse_question(
        cls,
        raw_question: dict,
        question_order: int,
    ) -> AssessmentQuestion:

        question_type = str(
            raw_question.get(
                "question_type",
            )
            or "",
        ).strip()

        question = str(
            raw_question.get(
                "question",
            )
            or "",
        ).strip()

        content = str(
            raw_question.get(
                "content",
            )
            or "",
        ).strip()

        answer = str(
            raw_question.get(
                "answer",
            )
            or "",
        )

        if not question:
            raise ValueError(
                f"Câu hỏi {question_order}: " "question không được để trống."
            )

        if not answer.strip():
            raise ValueError(
                f"Câu hỏi {question_order}: " "answer không được để trống."
            )

        score = cls.parse_score(
            raw_question.get("score"),
            question_order,
        )

        raw_options = [line.strip() for line in answer.splitlines() if line.strip()]

        if question_type == "multiple_choice":
            return cls.parse_multiple_choice(
                question=question,
                content=content,
                raw_options=raw_options,
                question_order=question_order,
                score=score,
            )

        if question_type == "ordering":
            return cls.parse_ordering(
                question=question,
                content=content,
                raw_options=raw_options,
                question_order=question_order,
                score=score,
            )

        if question_type == "drag_and_drop":
            return cls.parse_drag_and_drop(
                question=question,
                content=content,
                raw_options=raw_options,
                question_order=question_order,
                score=score,
            )

        raise ValueError(
            f"Câu hỏi {question_order}: "
            f"question_type '{question_type}' "
            "không được hỗ trợ."
        )

    @staticmethod
    def parse_score(
        raw_score,
        question_order: int,
    ) -> Decimal:

        if raw_score is None or raw_score == "":
            return Decimal("0.00")

        try:
            score = Decimal(str(raw_score))
        except Exception as error:
            raise ValueError(
                f"Câu hỏi {question_order}: " "score không hợp lệ."
            ) from error

        if score < Decimal("0.00"):
            raise ValueError(f"Câu hỏi {question_order}: " "score không được âm.")

        return score

    @classmethod
    def normalize_option(
        cls,
        raw_option: str,
    ) -> tuple[bool, str]:

        value = str(
            raw_option or "",
        ).strip()

        if not value:
            raise ValueError("Đáp án không được để trống.")

        is_correct = value.startswith("*")

        if is_correct:
            value = value[1:].strip()

        match = cls.OPTION_PREFIX_PATTERN.match(value)

        if match:
            value = match.group(2).strip()

        if not value:
            raise ValueError("Nội dung đáp án không được để trống.")

        return (
            is_correct,
            value,
        )

    @classmethod
    def build_options(
        cls,
        raw_options: list[str],
    ):

        options = []
        correct_ids = []

        for index, raw in enumerate(
            raw_options,
            start=1,
        ):
            is_correct, content = cls.normalize_option(
                raw,
            )

            option_id = f"OPT{index:04d}"

            options.append(
                AssessmentQuestionOption(
                    option_id=option_id,
                    content=content,
                    order=index,
                )
            )

            if is_correct:
                correct_ids.append(
                    option_id,
                )

        return (
            options,
            correct_ids,
        )

    @staticmethod
    def build_question_content(
        question: str,
        content: str,
    ) -> str:

        if content:
            return f"{question}\n\n{content}"

        return question

    @classmethod
    def parse_multiple_choice(
        cls,
        question: str,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        if len(raw_options) < 2:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "multiple_choice phải có ít nhất 2 đáp án."
            )

        options, correct_ids = cls.build_options(
            raw_options,
        )

        if len(correct_ids) != 1:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "multiple_choice phải có đúng "
                "một đáp án bắt đầu bằng dấu *."
            )

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            question=question,
            content=content or None,
            question_type="multiple_choice",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=0,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_option_ids=correct_ids,
            ),
            test_cases=[],
        )

    @classmethod
    def parse_ordering(
        cls,
        question: str,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        if len(raw_options) < 2:
            raise ValueError(
                f"Câu hỏi {question_order}: " "ordering phải có ít nhất 2 đáp án."
            )

        if any(line.startswith("*") for line in raw_options):
            raise ValueError(
                f"Câu hỏi {question_order}: " "ordering không được sử dụng dấu *."
            )

        options, _ = cls.build_options(
            raw_options,
        )

        correct_order_ids = [option.option_id for option in options]

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            question=question,
            content=content or None,
            question_type="ordering",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=0,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_order_option_ids=correct_order_ids,
            ),
            test_cases=[],
        )

    @classmethod
    def parse_drag_and_drop(
        cls,
        question: str,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        if not content:
            raise ValueError(
                f"Câu hỏi {question_order}: " "drag_and_drop bắt buộc phải có content."
            )

        blank_count = content.count("___")

        if blank_count < 1:
            raise ValueError(
                f"Câu hỏi {question_order}: " "drag_and_drop phải có ít nhất một ___."
            )

        options, correct_ids = cls.build_options(
            raw_options,
        )

        if len(correct_ids) != blank_count:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                f"có {blank_count} vị trí ___ "
                f"nhưng có {len(correct_ids)} "
                "đáp án đúng."
            )

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            question=question,
            content=content,
            question_type="drag_and_drop",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=blank_count,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_option_ids=correct_ids,
            ),
            test_cases=[],
        )
