from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from datetime import datetime

@dataclass
class AssignmentListDTO:
    assignment_id: str
    subject_name: str
    title: str
    description: Optional[str]
    assignment_type: str
    total_score: Decimal
    status: str
    is_active: bool
    created_at: datetime