from dataclasses import dataclass
from typing import Optional


@dataclass
class AssessmentQuestionTestCase:

    test_case_id: str
    expected_output: str
    order: int

    input: Optional[str] = None
    is_hidden: bool = True