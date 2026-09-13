from dataclasses import dataclass
from datetime import date


@dataclass
class CreateAcademicYearDTO:

    name: str
    start_date: date
    end_date: date