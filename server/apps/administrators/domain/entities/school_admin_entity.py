from dataclasses import dataclass
from typing import Optional


@dataclass
class SchoolAdmin:
    
    school_admin_id: str
    full_name: str
    gender: Optional[str]
    email: str
    phone: Optional[str]
    university_id: Optional[str]
    university_name: Optional[str]
    status: str = "active"