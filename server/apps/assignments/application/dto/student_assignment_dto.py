from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Any


@dataclass
class StudentAssignmentOptionDTO:

    option_id: str
    content: str
    order: int


@dataclass
class StudentAssignmentQuestionDTO:

    question_id: str
    question:str
    content: str
    question_type: str
    score: Decimal
    order: int
    shuffle_options: bool
    blank_count: int
    options: list[StudentAssignmentOptionDTO]

@dataclass
class StudentAssignmentReviewDTO:

    question_id: str
    question_type: str
    user_answer: Any
    correct: bool
    score: Decimal
    correct_answer: Any
@dataclass
class StudentAssignmentResultDTO:

    score: Decimal
    total_score: Decimal
    percentage: Decimal
    answered_count: int
    correct_count: int
    submitted_at: datetime | None
    review: list[StudentAssignmentReviewDTO]

@dataclass
class StudentAssignmentContentDTO:

    assignment_application_id: str
    assignment_id: str
    lesson_id: str

    title: str
    description: str | None

    subject_id: str
    subject_name: str

    assignment_type: str

    total_score: Decimal
    duration_minutes: int
    max_attempts: int

    open_at: datetime | None
    due_at: datetime | None

    attempt_id: str
    attempt_status: str

    remaining_seconds: int

    saved_answers: dict

    questions: list[StudentAssignmentQuestionDTO]

    result: StudentAssignmentResultDTO | None = None