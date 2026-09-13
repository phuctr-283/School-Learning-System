from dataclasses import dataclass
from datetime import date


@dataclass
class ImportClassSectionDTO:

    subject_name: str

    group_number: int

    teacher_name: str

    semester_name: str

    academic_year_name: str

    start_date: date

    end_date: date