class GetStudentLessonOpeningsUseCase:

    def __init__(
        self,
        class_section_lesson_plan_repository,
    ):
        self.class_section_lesson_plan_repository = class_section_lesson_plan_repository

    def execute(
        self,
        university_id: str,
        class_section_id: str,
        student_id: str,
    ):

        university_id = university_id.strip()
        class_section_id = class_section_id.strip()
        student_id = student_id.strip()

        if not university_id:
            raise ValueError("Thiếu mã trường.")

        if not class_section_id:
            raise ValueError("Thiếu mã lớp học phần.")

        if not student_id:
            raise ValueError("Thiếu mã sinh viên.")

        return self.class_section_lesson_plan_repository.get_student_lesson_openings(
            university_id=university_id,
            class_section_id=class_section_id,
            student_id=student_id,
        )
