class GetAssignmentContentUseCase:

    def __init__(
        self,
        assignment_repository,
    ):
        self.assignment_repository = (
            assignment_repository
        )

    def execute(
        self,
        assignment_id: str,
        university_id: str,
        teacher_email: str,
    ):

        if not assignment_id:
            raise ValueError(
                "Mã bài tập không được để trống.",
            )

        if not university_id:
            raise ValueError(
                "Mã trường đại học không được để trống.",
            )

        if not teacher_email:
            raise ValueError(
                "Không xác định được email giảng viên.",
            )

        assignment = (
            self.assignment_repository.get_content_by_id(
                assignment_id=assignment_id,
                university_id=university_id,
                teacher_email=teacher_email,
            )
        )

        if assignment is None:
            raise ValueError(
                "Không tìm thấy bài tập.",
            )

        return assignment