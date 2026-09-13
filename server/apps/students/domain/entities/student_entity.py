from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Student:

    student_id: str
    full_name: str
    gender: str
    student_class: str

    department_id: str
    department_name: str

    cohort_id: str
    status: str

    university_id: str
    university_name: str

    date_of_birth: Optional[date] = None
    email: Optional[str] = None
    phone: Optional[str] = None