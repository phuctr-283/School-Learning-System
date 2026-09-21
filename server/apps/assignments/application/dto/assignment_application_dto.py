from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssignmentApplicationDTO:

    assignment_application_id: str

    assignment_id: str

    class_section_ids: list[str]

    lesson_id: str

    status: str

    open_at: datetime | None

    due_at: datetime | None

    max_attempts: int