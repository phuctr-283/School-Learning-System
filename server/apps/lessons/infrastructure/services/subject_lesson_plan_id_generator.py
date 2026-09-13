from apps.lessons.infrastructure.persistence.models.subject_lesson_plan_model import (
    SubjectLessonPlanModel,
)


class SubjectLessonPlanIdGenerator:

    PREFIX = "SLP"

    def generate(
        self,
        university,
    ) -> str:

        plans = SubjectLessonPlanModel.objects(
            university=university,
        )

        max_number = 0

        for plan in plans:

            value = plan.subject_lesson_plan_id

            if not value.startswith(self.PREFIX):
                continue

            number_part = value[
                len(self.PREFIX):
            ]

            if not number_part.isdigit():
                continue

            max_number = max(
                max_number,
                int(number_part),
            )

        return f"{self.PREFIX}{max_number + 1:03d}"