class GetLessonOpeningsUseCase:

    def __init__(
        self,
        lesson_opening_repository,
    ):

        self.lesson_opening_repository = (
            lesson_opening_repository
        )


    def execute(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):

        return (
            self.lesson_opening_repository
            .get_by_class_section_lesson_plan(
                university_id=university_id,

                class_section_lesson_plan_id=(
                    class_section_lesson_plan_id
                ),
            )
        )