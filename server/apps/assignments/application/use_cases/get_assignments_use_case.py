class GetAssignmentsUseCase:

    def __init__(
        self,
        assignment_repository,
    ):
        self.assignment_repository = assignment_repository

    def execute(
        self,
        university_id: str,
        teacher_id: str,
        department_id: str | None = None,
    ):

        return self.assignment_repository.get_by_teacher(
            teacher_id=teacher_id,
            university_id=university_id,
            department_id=department_id,
        )