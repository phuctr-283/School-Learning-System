class EnsureLessonPlansUseCase:

    def __init__(
        self,
        ensure_course_lesson_plans_use_case,
        ensure_class_section_lesson_plans_use_case,
        ensure_lesson_openings_use_case,
    ):
        self.ensure_course_lesson_plans_use_case = (
            ensure_course_lesson_plans_use_case
        )

        self.ensure_class_section_lesson_plans_use_case = (
            ensure_class_section_lesson_plans_use_case
        )

        self.ensure_lesson_openings_use_case = (
            ensure_lesson_openings_use_case
        )


    def execute(
        self,
        university_id: str,
    ):

        # =====================================================
        # 1. COURSE LESSON PLAN
        # =====================================================

        course_lesson_plans = (
            self.ensure_course_lesson_plans_use_case.execute(
                university_id=university_id,
            )
        )


        # =====================================================
        # 2. CLASS SECTION LESSON PLAN
        # =====================================================

        class_section_lesson_plans = (
            self.ensure_class_section_lesson_plans_use_case.execute(
                university_id=university_id,
            )
        )


        # =====================================================
        # 3. LESSON OPENING
        # =====================================================

        lesson_openings = (
            self.ensure_lesson_openings_use_case.execute(
                university_id=university_id,
            )
        )


        return {
            "course_lesson_plans": course_lesson_plans,

            "class_section_lesson_plans": (
                class_section_lesson_plans
            ),

            "lesson_openings": lesson_openings,
        }