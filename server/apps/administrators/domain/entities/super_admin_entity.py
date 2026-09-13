from dataclasses import dataclass
from typing import Optional

@dataclass
class SuperAdmin:

    super_admin_id: str
    full_name: str
    email: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    status: str = "active"