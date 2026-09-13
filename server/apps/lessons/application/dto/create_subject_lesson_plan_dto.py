from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateSubjectLessonPlanRuleDTO:

    lesson_type: str

    min_credits: Optional[int]

    max_credits: Optional[int]

    total_lessons: int

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "CreateSubjectLessonPlanRuleDTO":

        return cls(
            lesson_type=data["lesson_type"],
            min_credits=data.get("min_credits"),
            max_credits=data.get("max_credits"),
            total_lessons=data["total_lessons"],
        )


@dataclass
class CreateSubjectLessonPlanDTO:

    semester_number: str

    rules: list[CreateSubjectLessonPlanRuleDTO]

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "CreateSubjectLessonPlanDTO":

        rules = [
            CreateSubjectLessonPlanRuleDTO.from_dict(
                rule
            )
            for rule in data["rules"]
        ]

        return cls(
            semester_number=data["semester_number"],
            rules=rules,
        )