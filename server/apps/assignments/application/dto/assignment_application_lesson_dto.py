from dataclasses import dataclass


@dataclass
class AssignmentApplicationLessonDTO:

    assignment_application_id: str

    assignment_id: str

    class_section_id: str

    lesson_id: str

    title: str

    is_active: bool