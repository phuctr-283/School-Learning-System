class GetStudentClassSectionLessonsUseCase:

    def __init__(
        self,
        class_section_lesson_plan_repository,
    ):
        self.class_section_lesson_plan_repository = (
            class_section_lesson_plan_repository
        )

    def execute(
        self,
        student_id: str,
        university_id: str,
        class_section_id: str,
    ):

        student_id = str(
            student_id or ""
        ).strip()

        university_id = str(
            university_id or ""
        ).strip()

        class_section_id = str(
            class_section_id or ""
        ).strip()

        if not student_id:
            raise ValueError(
                "Mã sinh viên không được để trống."
            )

        if not university_id:
            raise ValueError(
                "Mã trường không được để trống."
            )

        if not class_section_id:
            raise ValueError(
                "Mã lớp học phần không được để trống."
            )

        return (
            self.class_section_lesson_plan_repository
            .get_student_lessons(
                student_id=student_id,
                university_id=university_id,
                class_section_id=class_section_id,
            )
        )