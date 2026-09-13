from dataclasses import dataclass


@dataclass
class CourseLessonPlanDTO:
    course_lesson_plan_id: str

    university_id: str
    university_name: str

    subject_id: str
    subject_name: str

    semester_id: str
    semester_name: str
    semester_number: str

    academic_year_id: str
    academic_year_name: str

    total_lessons: int