from dataclasses import dataclass


@dataclass
class StudentClassSectionDTO:
    class_section_id: str
    academic_year_id: str
    semester_id: str
    subject_id: str
    group_number: int
    subject_name: str
    teacher_name: str