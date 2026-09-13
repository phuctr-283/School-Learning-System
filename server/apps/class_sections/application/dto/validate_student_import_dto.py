from dataclasses import dataclass


@dataclass
class ValidateStudentImportDTO:

    student_id: str

    full_name: str

    student_class: str