from dataclasses import dataclass


@dataclass
class LessonDTO:

    lesson_id: str

    lesson_number: int

    name: str

    university_id: str