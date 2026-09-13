from dataclasses import dataclass
from typing import List


@dataclass
class CreateSemesterLessonPlanItemDTO:

    semester_number: str

    total_lessons: int


@dataclass
class CreateSemesterLessonPlanDTO:

    academic_year_id: str

    semesters: List[
        CreateSemesterLessonPlanItemDTO
    ]