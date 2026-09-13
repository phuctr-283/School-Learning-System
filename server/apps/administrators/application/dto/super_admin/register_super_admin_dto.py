from dataclasses import dataclass


@dataclass
class RegisterSuperAdminDTO:

    full_name: str
    username: str
    password: str