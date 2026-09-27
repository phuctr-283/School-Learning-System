from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Any


@dataclass
class AssignmentHistoryOptionDTO:
    
    option_id: str
    content: str
    is_correct: bool
    is_selected: bool
    is_selected_correct: bool
    is_selected_wrong: bool

@dataclass
class AssignmentHistoryQuestionDTO:
    
    question_id: str
    question: str
    content: str
    question_type: str
    score: Decimal
    earned_score: Decimal
    user_answer: Any
    correct_answer: Any
    correct: bool
    options: list[AssignmentHistoryOptionDTO]
    correct_options: list[AssignmentHistoryOptionDTO]
    wrong_options: list[AssignmentHistoryOptionDTO]
    
@dataclass
class AssignmentHistoryDTO:

    attempt_id: str
    assignment_application_id: str
    assignment_id: str
    lesson_id: str
    title: str
    subject_name: str
    assignment_type: str
    total_score: Decimal
    score: Decimal
    percentage: Decimal
    answered_count: int
    correct_count: int
    started_at: datetime
    submitted_at: datetime | None
    questions: list[AssignmentHistoryQuestionDTO]