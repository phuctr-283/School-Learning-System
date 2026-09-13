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
        department_id: str,
        teacher_id: str,
    ):
        return (
            self.class_section_repository
            .get_teacher_subjects(
                university_id=university_id,
                department_id=department_id,
                teacher_id=teacher_id,
            )
        )