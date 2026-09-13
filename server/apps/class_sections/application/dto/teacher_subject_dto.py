from dataclasses import dataclass


@dataclass
class TeacherSubjectDTO:
    university_id: str
    department_id: str
    subject_id: str
    subject_name: str