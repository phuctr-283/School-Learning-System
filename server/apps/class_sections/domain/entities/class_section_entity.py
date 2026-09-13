from dataclasses import dataclass
from datetime import date


@dataclass
class ClassSection:

    class_section_id: str

    subject_id: str
    subject_name: str

    group_number: int

    teacher_id: str
    teacher_name: str

    semester_id: str
    semester_name: str
    semester_number: str

    academic_year_id: str
    academic_year_name: str

    university_id: str
    university_name: str

    start_date: date
    end_date: date

    status: str