class UpdateAssignmentApplicationClassSectionStatusUseCase:

    def __init__(
        self,
        assignment_application_repository,
    ):
        self.assignment_application_repository = assignment_application_repository

    def execute(
        self,
        assignment_application_id: str,
        class_section_id: str,
        teacher_email: str,
        status: str,
    ):

        if status not in (
            "active",
            "closed",
        ):
            raise ValueError("Trạng thái phải là active hoặc closed.")

        return self.assignment_application_repository.update_class_section_status(
            assignment_application_id=(assignment_application_id),
            class_section_id=class_section_id,
            teacher_email=teacher_email,
            status=status,
        )
