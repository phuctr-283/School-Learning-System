from dataclasses import dataclass

from apps.lessons.application.dto.lesson_opening_dto import (
    LessonOpeningDTO,
)


@dataclass
class StudentClassSectionLessonDTO:

    class_section_id: str

    academic_year_id: str
    academic_year_name: str

    semester_id: str
    semester_name: str
    semester_number: str

    subject_id: str
    subject_name: str

    group_number: int

    lesson_openings: list[LessonOpeningDTO]