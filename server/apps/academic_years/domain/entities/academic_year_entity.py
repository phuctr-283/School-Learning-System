from dataclasses import dataclass
from datetime import date


@dataclass
class AcademicYear:

    academic_year_id: str
    university_id: str
    university_name: str
    name: str
    start_date: date
    end_date: date
    status: str