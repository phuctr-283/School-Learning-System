from apps.lessons.application.dto.course_lesson_plan_dto import (
    CourseLessonPlanDTO,
)


class GetCourseLessonPlansUseCase:

    def __init__(
        self,
        course_lesson_plan_repository,
    ):
        self.course_lesson_plan_repository = (
            course_lesson_plan_repository
        )

    def execute(
        self,
        university_id: str,
    ):

        if not university_id:
            raise ValueError(
                "University ID không được để trống."
            )

        plans = (
            self.course_lesson_plan_repository
            .get_by_university(
                university_id=university_id,
            )
        )

        return [
            CourseLessonPlanDTO(
                course_lesson_plan_id=plan.course_lesson_plan_id,

                university_id=plan.university_id,
                university_name=plan.university_name,

                subject_id=plan.subject_id,
                subject_name=plan.subject_name,

                semester_id=plan.semester_id,
                semester_name=plan.semester_name,
                semester_number=plan.semester_number,

                academic_year_id=plan.academic_year_id,
                academic_year_name=plan.academic_year_name,

                total_lessons=plan.total_lessons,
            )
            for plan in plans
        ]