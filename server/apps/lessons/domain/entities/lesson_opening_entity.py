from dataclasses import dataclass
from datetime import datetime


@dataclass
class LessonOpening:

    lesson_id: str
    lesson_number: int
    lesson_name: str

    status: str

    opened_at: datetime | None
    closed_at: datetime | None