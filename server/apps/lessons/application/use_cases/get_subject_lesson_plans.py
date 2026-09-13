from apps.lessons.application.dto.subject_lesson_plan_dto import (
    SubjectLessonPlanDTO,
)

from apps.lessons.domain.repositories.subject_lesson_plan_repository import (
    SubjectLessonPlanRepository,
)


class GetSubjectLessonPlansUseCase:

    def __init__(
        self,
        repository: SubjectLessonPlanRepository,
    ):
        self.repository = repository

    def execute(
        self,
        university_id: str,
    ) -> list[SubjectLessonPlanDTO]:

        plans = self.repository.get_subject_lesson_plans(
            university_id=university_id,
        )

        return [
            SubjectLessonPlanDTO(
                subject_lesson_plan_id=(plan.subject_lesson_plan_id),
                university_id=(plan.university.university_id),
                semester_number=(plan.semester_number),
                lesson_type=(plan.lesson_type),
                min_credits=(plan.min_credits),
                max_credits=(plan.max_credits),
                total_lessons=(plan.total_lessons),
                is_custom=(plan.is_custom),
            )
            for plan in plans
        ]
