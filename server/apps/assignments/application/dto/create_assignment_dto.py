from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CreateAssignmentDTO:

    university_id: str

    department_id: str

    subject_id: str

    teacher_id: str

    title: str

    questions: list[dict[str, Any]]

    assignment_type: str = "practice"

    description: Optional[str] = None