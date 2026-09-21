from apps.lessons.application.dto.class_section_lesson_plan_dto import (
    ClassSectionLessonPlanDTO,
)

from apps.lessons.application.dto.lesson_opening_dto import (
    LessonOpeningDTO,
)


class GetClassSectionLessonPlansUseCase:

    def __init__(
        self,
        class_section_lesson_plan_repository,
    ):

        self.class_section_lesson_plan_repository = class_section_lesson_plan_repository

    def execute(
        self,
        university_id: str,
        course_lesson_plan_id: str,
    ):

        if not university_id:
            raise ValueError("University ID không được để trống.")

        if not course_lesson_plan_id:
            raise ValueError("Course lesson plan ID " "không được để trống.")

        plans = self.class_section_lesson_plan_repository.get_by_course_lesson_plan(
            university_id=university_id,
            course_lesson_plan_id=(course_lesson_plan_id),
        )

        return [
            ClassSectionLessonPlanDTO(
                class_section_lesson_plan_id=(plan.class_section_lesson_plan_id),
                university_id=plan.university_id,
                university_name=plan.university_name,
                course_lesson_plan_id=(plan.course_lesson_plan_id),
                class_section_id=(plan.class_section_id),
                group_number=(plan.group_number),
                subject_id=plan.subject_id,
                subject_name=plan.subject_name,
                semester_id=plan.semester_id,
                semester_name=plan.semester_name,
                semester_number=plan.semester_number,
                academic_year_id=(plan.academic_year_id),
                academic_year_name=(plan.academic_year_name),
                total_lessons=(plan.total_lessons),
                is_custom=(plan.is_custom),
                custom_total_lessons=(plan.custom_total_lessons),
                effective_total_lessons=(plan.effective_total_lessons),
                lesson_openings=[
                    LessonOpeningDTO(
                        lesson_id=(opening.lesson_id),
                        lesson_number=(opening.lesson_number),
                        lesson_name=(opening.lesson_name),
                        status=(opening.status),
                        opened_at=(opening.opened_at),
                        closed_at=(opening.closed_at),
                    )
                    for opening in (plan.lesson_openings or [])
                ],
            )
            for plan in plans
        ]
