from dataclasses import dataclass


@dataclass
class AssessmentQuestionOption:

    option_id: str
    content: str
    order: int