class GetAssignmentApplicationsUseCase:

    def __init__(
        self,
        assignment_application_repository,
    ):
        self.assignment_application_repository = (
            assignment_application_repository
        )

    def execute(
        self,
        class_section_id: str,
        lesson_id: str,
        teacher_email: str,
    ):

        if not class_section_id:
            raise ValueError(
                "Thiếu mã lớp học phần."
            )

        if not lesson_id:
            raise ValueError(
                "Thiếu mã lesson."
            )

        if not teacher_email:
            raise ValueError(
                "Không xác định được tài khoản giáo viên."
            )

        return (
            self.assignment_application_repository
            .get_by_class_section_and_lesson(
                class_section_id=class_section_id,
                lesson_id=lesson_id,
                teacher_email=teacher_email,
            )
        )