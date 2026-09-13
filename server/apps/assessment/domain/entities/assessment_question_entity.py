from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from apps.assessment.domain.entities.assessment_question_option_entity import (
    AssessmentQuestionOption,
)

from apps.assessment.domain.entities.assessment_question_answer_entity import (
    AssessmentQuestionAnswer,
)

from apps.assessment.domain.entities.assessment_question_test_case_entity import (
    AssessmentQuestionTestCase,
)


@dataclass
class AssessmentQuestion:

    question_id: str
    content: str
    question_type: str
    score: Decimal
    order: int

    shuffle_options: bool = False
    blank_count: int = 0

    options: list[AssessmentQuestionOption] = field(
        default_factory=list,
    )

    answer: Optional[AssessmentQuestionAnswer] = None

    test_cases: list[AssessmentQuestionTestCase] = field(
        default_factory=list,
    )