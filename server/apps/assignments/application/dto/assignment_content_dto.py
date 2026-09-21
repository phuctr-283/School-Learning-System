from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class AssignmentContentDTO:

    assignment_id: str

    university_id: str
    subject_id: str
    subject_name: str

    teacher_id: str

    title: str
    description: Optional[str]

    assignment_type: str

    total_score: Decimal
    duration_minutes: int

    status: str
    is_active: bool

    created_at: datetime | None
    updated_at: datetime | None