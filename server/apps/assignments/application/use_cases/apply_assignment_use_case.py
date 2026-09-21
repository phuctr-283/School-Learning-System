class ApplyAssignmentUseCase:

    def __init__(
        self,
        assignment_application_repository,
    ):
        self.assignment_application_repository = (
            assignment_application_repository
        )

    def execute(
        self,
        dto,
    ):

        return (
            self.assignment_application_repository
            .apply_to_class_sections(
                assignment_id=dto.assignment_id,
                lesson_id=dto.lesson_id,
                class_section_ids=dto.class_section_ids,
                teacher_email=dto.teacher_email,
                max_attempts=dto.max_attempts,
            )
        )