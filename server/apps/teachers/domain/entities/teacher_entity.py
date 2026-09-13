from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Teacher:

    teacher_id: str
    full_name: str
    gender: Optional[str]
    date_of_birth: Optional[date]
    email: Optional[str]
    phone: Optional[str]
    department_id: str
    department_name: str
    university_id: str
    university_name: str
    status: str
