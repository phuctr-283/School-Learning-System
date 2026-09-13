from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateSubjectDTO:

    subject_id: str
    name: str

    department_id: str

    subject_types: str
    credits: int

    process_percent: Decimal
    midterm_percent: Decimal
    final_percent: Decimal