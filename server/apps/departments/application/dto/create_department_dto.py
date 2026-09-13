from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateDepartmentDTO:

    department_id: str
    department_number: str
    name: str
    head_id: Optional[str] = None