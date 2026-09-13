from dataclasses import dataclass
from typing import Optional


@dataclass
class ClassSectionLessonPlanDTO:
    class_section_lesson_plan_id: str

    university_id: str
    university_name: str

    course_lesson_plan_id: str

    class_section_id: str
    group_number: int

    subject_id: str
    subject_name: str

    semester_id: str
    semester_name: str
    semester_number: str

    academic_year_id: str
    academic_year_name: str

    total_lessons: int

    is_custom: bool
    custom_total_lessons: Optional[int]

    effective_total_lessons: int