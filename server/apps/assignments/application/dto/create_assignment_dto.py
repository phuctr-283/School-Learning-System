from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateAssignmentDTO:
    title: str
    description: Optional[str]
    subject_id: str
    assignment_type: str
    duration_minutes: int
    questions: list[dict]