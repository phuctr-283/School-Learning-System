from dataclasses import dataclass
from typing import Any, Optional
from decimal import Decimal

@dataclass
class AssignmentDTO:

    assignment_id: str

    university_id: str
    subject_id: str
    subject_name: str

    teacher_id: str

    title: str

    questions: list[dict[str, Any]]

    total_score: Decimal

    assignment_type: str
    status: str
    is_active: bool

    created_at: str
    updated_at: str

    description: Optional[str] = None