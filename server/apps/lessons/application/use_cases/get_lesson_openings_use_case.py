from apps.lessons.application.dto.lesson_opening_dto import (
    LessonOpeningDTO,
)


class GetLessonOpeningsUseCase:

    def __init__(
        self,
        class_section_lesson_plan_repository,
    ):

        self.class_section_lesson_plan_repository = (
            class_section_lesson_plan_repository
        )

    def execute(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):

        if not university_id:
            raise ValueError(
                "University ID không được để trống."
            )

        if not class_section_lesson_plan_id:
            raise ValueError(
                "Class section lesson plan ID "
                "không được để trống."
            )

        plan = (
            self.class_section_lesson_plan_repository
            .get_by_class_section_lesson_plan_id(
                university_id=university_id,
                class_section_lesson_plan_id=(
                    class_section_lesson_plan_id
                ),
            )
        )

        if not plan:
            raise ValueError(
                "Không tìm thấy kế hoạch lớp học phần."
            )

        return [
            LessonOpeningDTO(
                lesson_id=opening.lesson_id,
                lesson_number=opening.lesson_number,
                lesson_name=opening.lesson_name,
                status=opening.status,
                opened_at=opening.opened_at,
                closed_at=opening.closed_at,
            )
            for opening in (
                plan.lesson_openings or []
            )
        ]