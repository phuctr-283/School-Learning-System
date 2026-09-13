from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SubjectDTO:
    subject_id: str
    name: str

    university_id: str
    university_name: str

    department_id: str
    department_name: str

    subject_types: str
    credits: int

    process_percent: Decimal
    midterm_percent: Decimal
    final_percent: Decimal

    status: str