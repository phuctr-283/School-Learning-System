from dataclasses import dataclass


@dataclass
class TeacherClassSectionDTO:
    university_id: str
    department_id: str

    class_section_id: str

    academic_year_id: str
    academic_year_name: str

    semester_id: str
    semester_name: str
    semester_number: str

    subject_id: str
    subject_name: str

    group_number: int
    status: str