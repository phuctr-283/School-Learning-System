from dataclasses import dataclass


@dataclass
class SemesterLessonPlan:

    semester_lesson_plan_id: str

    university_id: str

    semester_id: str

    academic_year_id: str
    academic_year_name: str

    semester_number: str
    semester_name: str
    
    total_lessons: int