class GetAssignmentsUseCase:

    def __init__(self, assignment_repository):
        self.assignment_repository = assignment_repository

    def execute(
        self,
        university_id: str,
        teacher_email: str,
    ):
        return self.assignment_repository.get_assignments(
            university_id=university_id,
            teacher_email=teacher_email,
        )