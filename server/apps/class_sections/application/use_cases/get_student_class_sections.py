class GetStudentClassSectionsUseCase:

    def __init__(
        self,
        class_section_student_repository,
    ):
        self.class_section_student_repository = (
            class_section_student_repository
        )

    def execute(
        self,
        student_id: str,
        university_id: str,
    ):
        student_id = str(student_id or "").strip()
        university_id = str(university_id or "").strip()

        if not student_id:
            raise ValueError(
                "Mã sinh viên không được để trống"
            )

        if not university_id:
            raise ValueError(
                "Mã trường không được để trống"
            )

        return (
            self.class_section_student_repository
            .get_student_class_sections(
                student_id=student_id,
                university_id=university_id,
            )
        )