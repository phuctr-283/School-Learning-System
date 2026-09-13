from dataclasses import dataclass
from datetime import date


@dataclass
class SemesterDTO:

    semester_id: str
    name: str
    semester_number: str
    academic_year_id: str
    academic_year_name: str
    university_id: str
    university_name: str
    start_date: date
    end_date: date
    status: str