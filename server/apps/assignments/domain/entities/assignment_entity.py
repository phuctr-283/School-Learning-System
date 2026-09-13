from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional

from apps.assessment.domain.entities.assessment_question_entity import (
    AssessmentQuestion,
)


@dataclass
class Assignment:

    assignment_id: str

    university_id: str
    department_id: str
    subject_id: str
    teacher_id: str

    title: str

    questions: list[AssessmentQuestion] = field(
        default_factory=list,
    )

    total_score: Decimal = Decimal("10.00")

    assignment_type: str = "practice"

    status: str = "draft"

    is_active: bool = True

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    description: Optional[str] = None