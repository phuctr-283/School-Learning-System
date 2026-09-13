from dataclasses import dataclass


@dataclass
class ValidatedStudent:

    row_number: int

    student_id: str

    full_name: str

    gender: str

    email: str

    student_class: str

    department_number: str

    cohort_id: str

    department: object