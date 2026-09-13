from dataclasses import dataclass
from typing import Optional

@dataclass
class Department:

    department_id: str
    department_number: str
    name: str
    university_id: str
    university_name: str
    head_id: Optional[str] = None
    head_name: Optional[str] = None
    is_active: bool = True