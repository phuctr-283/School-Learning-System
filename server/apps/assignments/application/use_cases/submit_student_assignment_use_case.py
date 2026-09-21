class SubmitStudentAssignmentUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        student_id,
        assignment_application_id,
        class_section_id,
        lesson_id,
        attempt_id,
        answers,
    ):

        return self.repository.submit_assignment(
            student_id=student_id,
            assignment_application_id=assignment_application_id,
            class_section_id=class_section_id,
            lesson_id=lesson_id,
            attempt_id=attempt_id,
            answers=answers,
        )