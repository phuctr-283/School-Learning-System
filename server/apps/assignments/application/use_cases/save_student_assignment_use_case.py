class SaveStudentAssignmentUseCase:

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

        return self.repository.save_answers(
            student_id=student_id,
            assignment_application_id=assignment_application_id,
            class_section_id=class_section_id,
            lesson_id=lesson_id,
            attempt_id=attempt_id,
            answers=answers,
        )