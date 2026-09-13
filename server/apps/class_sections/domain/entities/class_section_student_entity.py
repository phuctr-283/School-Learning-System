from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClassSectionStudent:

    class_section_id: str

    student_id: str

    created_at: Optional[datetime] = None