class GetAssignmentsBySubjectUseCase:

    def __init__(self, assignment_repository):
        self.assignment_repository = assignment_repository

    def execute(
        self,
        university_id: str,
        teacher_email: str,
        subject_id: str,
    ):
        normalized_subject_id = (subject_id or "").strip()

        if not normalized_subject_id:
            raise ValueError(
                "Không xác định được môn học.",
            )

        return self.assignment_repository.get_assignments_by_subject(
            university_id=university_id,
            teacher_email=teacher_email,
            subject_id=normalized_subject_id,
        )