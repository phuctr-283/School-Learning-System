import re

from decimal import Decimal, ROUND_HALF_UP

from apps.assessment.domain.entities.assessment_question_entity import (
    AssessmentQuestion,
)

from apps.assessment.domain.entities.assessment_question_option_entity import (
    AssessmentQuestionOption,
)

from apps.assessment.domain.entities.assessment_question_answer_entity import (
    AssessmentQuestionAnswer,
)


class QuestionParserService:

    OPTION_PREFIX_PATTERN = re.compile(r"^\s*([A-Da-d])(?:[\.\)])\s*(.*)$")

    SUPPORTED_QUESTION_TYPES = {
        "multiple_choice",
        "ordering",
        "drag_and_drop",
    }

    @classmethod
    def parse_questions(
        cls,
        raw_questions: list[dict],
    ) -> list[AssessmentQuestion]:

        if not raw_questions:
            raise ValueError("Danh sách câu hỏi không được để trống.")

        parsed_questions: list[AssessmentQuestion] = []

        for index, raw_question in enumerate(
            raw_questions,
            start=1,
        ):
            question = cls.parse_question(
                raw_question=raw_question,
                question_order=index,
            )

            parsed_questions.append(question)

        cls.assign_scores_if_missing(
            questions=parsed_questions,
        )

        return parsed_questions

    @classmethod
    def parse_question(
        cls,
        raw_question: dict,
        question_order: int,
    ) -> AssessmentQuestion:

        question_type = (raw_question.get("question_type") or "").strip()

        if question_type not in cls.SUPPORTED_QUESTION_TYPES:
            raise ValueError(
                f"Câu hỏi {question_order} có loại "
                f"'{question_type}' chưa được hỗ trợ."
            )

        content = (raw_question.get("content") or "").strip()

        if not content:
            raise ValueError(f"Câu hỏi {question_order} chưa có nội dung.")

        raw_options = raw_question.get(
            "options",
            [],
        )

        if not isinstance(raw_options, list):
            raise ValueError(f"Câu hỏi {question_order}: " "options phải là danh sách.")

        raw_score = raw_question.get("score")

        if raw_score is None:
            score = Decimal("0.00")
        else:
            try:
                score = Decimal(str(raw_score))
            except Exception as error:
                raise ValueError(
                    f"Câu hỏi {question_order}: " "điểm không hợp lệ."
                ) from error

        if score < Decimal("0.00"):
            raise ValueError(f"Câu hỏi {question_order}: " "điểm không được âm.")

        if question_type == "multiple_choice":
            return cls.parse_multiple_choice(
                content=content,
                raw_options=raw_options,
                question_order=question_order,
                score=score,
            )

        if question_type == "ordering":
            return cls.parse_ordering(
                content=content,
                raw_options=raw_options,
                question_order=question_order,
                score=score,
            )

        return cls.parse_drag_and_drop(
            content=content,
            raw_options=raw_options,
            question_order=question_order,
            score=score,
        )

    @classmethod
    def normalize_option(
        cls,
        raw_option: str,
    ) -> tuple[bool, str]:

        value = str(raw_option or "").strip()

        if not value:
            raise ValueError("Đáp án không được để trống.")

        is_correct = value.startswith("*")

        if is_correct:
            value = value[1:].strip()

        match = cls.OPTION_PREFIX_PATTERN.match(value)

        if match:
            value = match.group(2).strip()

        if not value:
            raise ValueError("Đáp án không được để trống.")

        return is_correct, value

    @classmethod
    def build_options(
        cls,
        raw_options: list[str],
    ) -> tuple[
        list[AssessmentQuestionOption],
        list[str],
    ]:

        options: list[AssessmentQuestionOption] = []
        correct_option_ids: list[str] = []

        for index, raw_option in enumerate(
            raw_options,
            start=1,
        ):
            is_correct, content = cls.normalize_option(
                raw_option=raw_option,
            )

            option_id = f"OPT{index:04d}"

            option = AssessmentQuestionOption(
                option_id=option_id,
                content=content,
                order=index,
            )

            options.append(option)

            if is_correct:
                correct_option_ids.append(option_id)

        return options, correct_option_ids

    @classmethod
    def parse_multiple_choice(
        cls,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        if len(raw_options) < 2:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "multiple_choice phải có ít nhất "
                "2 đáp án."
            )

        options, correct_option_ids = cls.build_options(raw_options)

        if len(correct_option_ids) != 1:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "multiple_choice phải có đúng "
                "một đáp án đúng."
            )

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            content=content,
            question_type="multiple_choice",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=0,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_option_ids=correct_option_ids,
            ),
            test_cases=[],
        )

    @classmethod
    def parse_ordering(
        cls,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        if len(raw_options) < 2:
            raise ValueError(
                f"Câu hỏi {question_order}: " "ordering phải có ít nhất " "2 đáp án."
            )

        options, correct_option_ids = cls.build_options(raw_options)

        if len(correct_option_ids) != len(options):
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "ordering phải đánh dấu * cho "
                "toàn bộ đáp án theo thứ tự đúng."
            )

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            content=content,
            question_type="ordering",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=0,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_order_option_ids=(correct_option_ids),
            ),
            test_cases=[],
        )

    @classmethod
    def parse_drag_and_drop(
        cls,
        content: str,
        raw_options: list[str],
        question_order: int,
        score: Decimal,
    ) -> AssessmentQuestion:

        blank_count = content.count("___")

        if blank_count == 0:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "drag_and_drop phải có ít nhất "
                "một vị trí ___."
            )

        if len(raw_options) < 2:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                "drag_and_drop phải có ít nhất "
                "2 đáp án."
            )

        options, correct_option_ids = cls.build_options(raw_options)

        if len(correct_option_ids) != blank_count:
            raise ValueError(
                f"Câu hỏi {question_order}: "
                f"có {blank_count} vị trí ___ nhưng "
                f"có {len(correct_option_ids)} đáp án đúng."
            )

        return AssessmentQuestion(
            question_id=f"Q{question_order:04d}",
            content=content,
            question_type="drag_and_drop",
            score=score,
            order=question_order,
            shuffle_options=True,
            blank_count=blank_count,
            options=options,
            answer=AssessmentQuestionAnswer(
                correct_option_ids=correct_option_ids,
            ),
            test_cases=[],
        )

    @classmethod
    def assign_scores_if_missing(
        cls,
        questions: list[AssessmentQuestion],
    ) -> None:

        if not questions:
            raise ValueError("Danh sách câu hỏi không được để trống.")

        scores = [question.score for question in questions]

        has_explicit_scores = [score > Decimal("0.00") for score in scores]

        if any(has_explicit_scores) and not all(has_explicit_scores):
            raise ValueError(
                "Phải nhập điểm cho tất cả câu hỏi " "hoặc không nhập điểm cho câu nào."
            )

        if all(has_explicit_scores):

            total_score = sum(
                scores,
                Decimal("0.00"),
            )

            if total_score != Decimal("10.00"):
                raise ValueError("Tổng điểm các câu hỏi phải bằng 10.")

            return

        question_count = len(questions)

        base_score = (Decimal("10.00") / Decimal(str(question_count))).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        remainder = Decimal("10.00") - base_score * question_count

        for index, question in enumerate(questions):
            question.score = base_score

            if index == question_count - 1:
                question.score += remainder
