class EnsureLessonPlansUseCase:

    def __init__(
        self,
        ensure_course_lesson_plans_use_case,
        ensure_class_section_lesson_plans_use_case,
    ):
        self.ensure_course_lesson_plans_use_case = (
            ensure_course_lesson_plans_use_case
        )

        self.ensure_class_section_lesson_plans_use_case = (
            ensure_class_section_lesson_plans_use_case
        )
    def execute(
        self,
        university_id: str,
    ):

        course_lesson_plans = (
            self.ensure_course_lesson_plans_use_case.execute(
                university_id=university_id,
            )
        )

        class_section_lesson_plans = (
            self.ensure_class_section_lesson_plans_use_case.execute(
                university_id=university_id,
            )
        )
        return {
            "course_lesson_plans": course_lesson_plans,

            "class_section_lesson_plans": (
                class_section_lesson_plans
            ),
        }