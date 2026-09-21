class GetTeacherActivePlannedClassSectionsUseCase:

    def __init__(
        self,
        class_section_repository,
    ):
        self.class_section_repository = class_section_repository

    def execute(
        self,
        university_id: str,
        username: str,
        subject_id: str,
        academic_year_id: str,
        semester_id: str,
    ):

        if not university_id:
            raise ValueError("Không xác định được trường đại học.")

        if not username:
            raise ValueError("Không xác định được tài khoản giảng viên.")

        if not subject_id:
            raise ValueError("Thiếu mã môn học.")

        if not academic_year_id:
            raise ValueError("Thiếu mã năm học.")

        if not semester_id:
            raise ValueError("Thiếu mã học kỳ.")

        return self.class_section_repository.get_teacher_active_planned_class_sections(
            university_id=university_id,
            username=username,
            subject_id=subject_id,
            academic_year_id=academic_year_id,
            semester_id=semester_id,
        )
