from dataclasses import dataclass
from typing import Optional


@dataclass
class SubjectLessonPlan:

    subject_lesson_plan_id: str

    university_id: str

    semester_number: str

    lesson_type: str

    min_credits: Optional[int]

    max_credits: Optional[int]

    total_lessons: int

    is_custom: bool = True