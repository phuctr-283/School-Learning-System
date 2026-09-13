from dataclasses import dataclass


@dataclass
class RegisterSchoolAdminDTO:

    full_name: str
    username: str
    password: str