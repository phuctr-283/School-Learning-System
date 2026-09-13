from dataclasses import dataclass


@dataclass
class SemesterLessonPlanDTO:

    semester_lesson_plan_id: str

    university_id: str

    academic_year_id: str

    academic_year_name: str

    semester_id: str

    semester_name: str

    semester_number: str

    total_lessons: int