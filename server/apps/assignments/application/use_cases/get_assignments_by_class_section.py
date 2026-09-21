class GetAssignmentsByClassSectionUseCase:

    def __init__(
        self,
        assignment_repository,
    ):
        self.assignment_repository = assignment_repository

    def execute(
        self,
        class_section_id: str,
    ):
        class_section_id = str(
            class_section_id or ""
        ).strip()

        if not class_section_id:
            raise ValueError(
                "Mã lớp học phần không được để trống"
            )

        return (
            self.assignment_repository
            .get_by_class_section_id(
                class_section_id=class_section_id,
            )
        )