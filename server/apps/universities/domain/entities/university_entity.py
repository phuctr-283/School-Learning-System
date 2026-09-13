from dataclasses import dataclass
from datetime import datetime


@dataclass
class University:

    university_id: str
    name: str
    domain: str
    email: str
    phone: str
    is_active: bool
    updated_at: datetime