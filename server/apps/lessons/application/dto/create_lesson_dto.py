from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateLessonDTO:

    create_mode: str

    lesson_number: Optional[int] = None

    lesson_number_start: Optional[int] = None

    lesson_number_end: Optional[int] = None