from dataclasses import dataclass


@dataclass
class SemesterContentDTO:

    semester_id: str
    name: str
    semester_number: str

    academic_year_id: str
    academic_year_name: str

    university_id: str
    university_name: str

    status: str