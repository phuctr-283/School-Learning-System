class VerifyStudentAssignmentQrUseCase:

    def __init__(
        self,
        assignment_application_repository,
    ):
        self.assignment_application_repository = (
            assignment_application_repository
        )

    def execute(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
    ):

        return (
            self.assignment_application_repository
            .verify_student_assignment_qr(
                student_id=student_id,
                assignment_application_id=(
                    assignment_application_id
                ),
                class_section_id=class_section_id,
                lesson_id=lesson_id,
            )
        )