from dataclasses import dataclass


@dataclass
class ApplyAssignmentDTO:

    assignment_id: str
    lesson_id: str
    class_section_ids: list[str]
    max_attempts: int
    teacher_email: str