class GetAssignmentByIdUseCase:

    def __init__(
        self,
        assignment_repository,
    ):
        self.assignment_repository = assignment_repository

    def execute(
        self,
        assignment_id: str,
        university_id: str,
        teacher_email: str,
    ):

        assignment_id = (
            assignment_id or ""
        ).strip()

        university_id = (
            university_id or ""
        ).strip()

        teacher_email = (
            teacher_email or ""
        ).strip().lower()

        if not assignment_id:
            raise ValueError(
                "Thiếu mã bài tập."
            )

        if not university_id:
            raise ValueError(
                "Không xác định được trường đại học."
            )

        if not teacher_email:
            raise ValueError(
                "Không xác định được email giảng viên."
            )

        assignment = (
            self.assignment_repository
            .get_by_id_for_teacher(
                assignment_id=assignment_id,
                university_id=university_id,
                teacher_email=teacher_email,
            )
        )

        if assignment is None:
            raise ValueError(
                "Không tìm thấy bài tập."
            )

        return assignment