from dataclasses import dataclass
from typing import Any, Optional
from decimal import Decimal

@dataclass
class AssignmentContentDTO:

    assignment_id: str
    title: str
    assignment_type: str
    subject_id: str
    teacher_id: str
    total_score: Decimal
    status: str
    questions: list[dict[str, Any]]

    description: Optional[str] = None