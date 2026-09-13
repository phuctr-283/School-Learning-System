from apps.lessons.application.dto.semester_lesson_plan_dto import (
    SemesterLessonPlanDTO,
)

from apps.lessons.domain.repositories.semester_lesson_plan_repository import (
    SemesterLessonPlanRepository,
)


class GetSemesterLessonPlansUseCase:

    def __init__(
        self,
        repository: SemesterLessonPlanRepository,
    ):
        self.repository = repository

    def execute(
        self,
        university_id: str,
    ) -> list[SemesterLessonPlanDTO]:

        plans = self.repository.get_by_university(
            university_id=university_id,
        )

        return [
            SemesterLessonPlanDTO(
                semester_lesson_plan_id=(
                    plan.semester_lesson_plan_id
                ),
                university_id=plan.university_id,
                academic_year_id=plan.academic_year_id,
                academic_year_name=plan.academic_year_name,
                semester_id=plan.semester_id,
                semester_name=plan.semester_name,
                semester_number=plan.semester_number,
                total_lessons=plan.total_lessons,
            )
            for plan in plans
        ]