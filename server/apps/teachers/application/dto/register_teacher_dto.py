from dataclasses import dataclass


@dataclass
class RegisterTeacherDTO:

    full_name: str
    university_id: str
    department_id: str
    email: str
    password: str