from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class AssignmentApplicationClassSectionDTO:

    class_section_id: str
    status: str
    opened_at: datetime | None
    closed_at: datetime | None

@dataclass
class AssignmentApplicationContentDTO:

    assignment_application_id: str
    assignment_id: str
    university_id: str
    lesson_id: str
    class_sections: list[AssignmentApplicationClassSectionDTO]
    title: str
    description: str | None
    subject_id: str
    subject_name: str
    assignment_type: str
    total_score: Decimal
    duration_minutes: int
    status: str
    max_attempts: int
    open_at: datetime | None
    due_at: datetime | None
    created_at: datetime
    updated_at: datetime

@dataclass
class AssignmentApplicationDTO:

    assignment_application_id: str
    assignment_id: str
    university_id: str
    lesson_id: str

    class_section_id: str
    class_section_status: str
    class_section_opened_at: datetime | None
    class_section_closed_at: datetime | None
    
    title: str
    description: str | None
    subject_id: str
    subject_name: str
    assignment_type: str
    total_score: Decimal
    duration_minutes: int
    status: str
    max_attempts: int
    open_at: datetime | None
    due_at: datetime | None
    created_at: datetime
    updated_at: datetime