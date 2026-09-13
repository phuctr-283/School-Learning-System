from dataclasses import dataclass
from typing import Optional


@dataclass
class DepartmentDTO:

    department_id: str
    department_number: str
    name: str
    university_id: str
    university_name: str
    head_id: Optional[str]
    head_name: Optional[str]
    is_active: bool