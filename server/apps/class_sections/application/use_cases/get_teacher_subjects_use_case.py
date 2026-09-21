class GetTeacherSubjectsUseCase:

    def __init__(
        self,
        class_section_repository,
    ):
        self.class_section_repository = (
            class_section_repository
        )

    def execute(
        self,
        university_id: str,
        username: str,
    ):
        if not university_id:
            raise ValueError(
                "Không xác định được trường đại học."
            )

        if not username:
            raise ValueError(
                "Không xác định được tài khoản giảng viên."
            )

        return (
            self.class_section_repository
            .get_teacher_subjects(
                university_id=university_id,
                username=username,
            )
        )