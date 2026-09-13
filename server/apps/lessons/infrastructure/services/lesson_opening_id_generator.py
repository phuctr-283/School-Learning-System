class LessonOpeningIdGenerator:

    def generate(
        self,
        class_section_lesson_plan_id: str,
        lesson_number: int,
    ):

        return (
            f"LO-"
            f"{class_section_lesson_plan_id}-"
            f"{lesson_number:02d}"
        )