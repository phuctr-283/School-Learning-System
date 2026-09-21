from django.utils import timezone


class UpdateLessonOpeningStatusUseCase:

    ALLOWED_STATUS = {
        "locked",
        "open",
        "closed",
    }

    def __init__(
        self,
        class_section_lesson_plan_repository,
    ):
        self.class_section_lesson_plan_repository = class_section_lesson_plan_repository

    def execute(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
        status: str,
    ):

        if not university_id:
            raise ValueError("University ID không được để trống.")

        if not class_section_lesson_plan_id:
            raise ValueError("Class section lesson plan ID " "không được để trống.")

        if not lesson_id:
            raise ValueError("Lesson ID không được để trống.")

        if status not in self.ALLOWED_STATUS:
            raise ValueError("Trạng thái buổi học không hợp lệ.")

        plan = self.class_section_lesson_plan_repository.get_by_class_section_lesson_plan_id(
            university_id=university_id,
            class_section_lesson_plan_id=class_section_lesson_plan_id,
        )

        if not plan:
            raise ValueError("Không tìm thấy kế hoạch buổi học.")

        opening = next(
            (item for item in plan.lesson_openings if item.lesson_id == lesson_id),
            None,
        )

        if not opening:
            raise ValueError("Không tìm thấy buổi học.")

        now = timezone.now()

        if status == "open":

            opened_at = opening.opened_at or now

            closed_at = None

        elif status == "closed":

            opened_at = opening.opened_at or now

            closed_at = now

        else:

            opened_at = None
            closed_at = None

        return self.class_section_lesson_plan_repository.update_lesson_opening_status(
            university_id=university_id,
            class_section_lesson_plan_id=class_section_lesson_plan_id,
            lesson_id=lesson_id,
            status=status,
            opened_at=opened_at,
            closed_at=closed_at,
        )
