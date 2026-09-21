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
    description: Optional[str] = None

    assignment_type: str = "practice"

    questions: list[AssessmentQuestion] = field(
        default_factory=list,
    )

    total_score: Decimal = Decimal("10.00")
    duration_minutes: int = 30

    status: str = "draft"
    is_active: bool = True

    created_at: datetime | None = None
    updated_at: datetime | None = None