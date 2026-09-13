from dataclasses import dataclass, field


@dataclass
class AssessmentQuestionAnswer:

    correct_option_ids: list[str] = field(
        default_factory=list,
    )

    correct_order_option_ids: list[str] = field(
        default_factory=list,
    )

    correct_answers: list[str] = field(
        default_factory=list,
    )