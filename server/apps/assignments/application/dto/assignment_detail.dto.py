from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class AssignmentQuestionDTO:
    question_type: str
    question: str
    content: str
    answer: str
    score: Decimal | None = None


@dataclass
class AssignmentDetailDTO:
    assignment_id: str
    university_id: str
    department_id: str
    subject_id: str
    teacher_id: str

    title: str
    description: Optional[str]

    assignment_type: str

    questions: list[AssignmentQuestionDTO]

    total_score: Decimal
    duration_minutes: int

    status: str
    is_active: bool

    created_at: object | None
    updated_at: object | None