from dataclasses import dataclass


@dataclass
class ImportStudentDTO:

    student_id: str

    full_name: str

    gender: str

    email: str

    student_class: str