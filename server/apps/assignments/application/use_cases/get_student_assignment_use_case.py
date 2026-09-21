class GetStudentAssignmentUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        student_id,
        assignment_application_id,
        class_section_id,
        lesson_id,
    ):

        return self.repository.get_student_assignment(
            student_id=student_id,
            assignment_application_id=assignment_application_id,
            class_section_id=class_section_id,
            lesson_id=lesson_id,
        )