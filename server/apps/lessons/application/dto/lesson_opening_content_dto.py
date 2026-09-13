from dataclasses import dataclass
from datetime import datetime


@dataclass
class LessonOpeningContentDTO:

    lesson_opening_id: str

    university_id: str
    university_name: str

    class_section_lesson_plan_id: str

    lesson_id: str
    lesson_number: int
    lesson_name: str

    status: str

    opened_at: datetime | None
    closed_at: datetime | None

    created_at: datetime
    updated_at: datetime