from dataclasses import dataclass
from datetime import datetime


@dataclass
class LessonOpening:

    lesson_opening_id: str

    university_id: str
    university_name: str

    class_section_lesson_plan_id: str

    lesson_id: str
    lesson_number: int
    lesson_name: str

    status: str

    opened_at: datetime | None = None
    closed_at: datetime | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None