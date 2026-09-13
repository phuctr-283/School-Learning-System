from dataclasses import dataclass
from datetime import date


@dataclass
class CreateSemesterDTO:

    academic_year_id: str

    semester_number: str

    start_date: date

    end_date: date