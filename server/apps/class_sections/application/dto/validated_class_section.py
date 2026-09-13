from dataclasses import dataclass
from datetime import date


@dataclass
class ValidatedClassSection:

    row_number: int

    subject: object
    teacher: object
    semester: object
    academic_year: object

    group_number: int

    start_date: date
    end_date: date

    is_existing: bool = False