from apps.subjects.domain.entities.subject_entity import (
    Subject,
)


class CreateSubjectUseCase:

    def __init__(
        self,
        subject_repository,
        university_repository,
        department_repository,
    ):
        self.subject_repository = subject_repository

        self.university_repository = university_repository

        self.department_repository = department_repository

    def execute(
        self,
        data,
        university_id: str,
    ):

        # =========================================
        # VALIDATE SUBJECT ID
        # =========================================

        if not data.subject_id:
            raise ValueError("Mã môn học không được để trống.")

        # =========================================
        # CHECK SUBJECT ID
        # =========================================

        if self.subject_repository.exists_by_id(
            data.subject_id,
        ):
            raise ValueError(f"Mã môn học {data.subject_id} đã tồn tại.")

        # =========================================
        # VALIDATE NAME
        # =========================================

        if not data.name:
            raise ValueError("Tên môn học không được để trống.")

        # =========================================
        # VALIDATE SUBJECT TYPE
        # =========================================

        if data.subject_types not in [
            "Theory",
            "Practice",
        ]:
            raise ValueError("Loại môn học không hợp lệ.")

        # =========================================
        # VALIDATE CREDITS
        # =========================================

        if data.credits < 1:
            raise ValueError("Số tín chỉ phải lớn hơn hoặc bằng 1.")

        # =========================================
        # VALIDATE SCORE PERCENT
        # =========================================

        total_percent = data.process_percent + data.midterm_percent + data.final_percent

        if total_percent != 100:
            raise ValueError("Tổng tỷ lệ điểm phải bằng 100%.")

        # =========================================
        # GET UNIVERSITY
        # =========================================

        university = self.university_repository.find_by_id(
            university_id,
        )

        if not university:
            raise ValueError("Không tìm thấy trường.")

        # =========================================
        # GET DEPARTMENT
        # =========================================

        department = self.department_repository.get_by_id(
            department_id=data.department_id,
            university_id=university_id,
        )

        if not department:
            raise ValueError("Không tìm thấy khoa thuộc trường.")

        # =========================================
        # CHECK DEPARTMENT ACTIVE
        # =========================================

        if not department.is_active:
            raise ValueError("Khoa đã ngừng hoạt động.")

        # =========================================
        # CREATE ENTITY
        # =========================================

        subject = Subject(
            subject_id=data.subject_id,
            name=data.name,
            university_id=university.university_id,
            university_name=university.name,
            department_id=department.department_id,
            department_name=department.name,
            subject_types=data.subject_types,
            credits=data.credits,
            process_percent=data.process_percent,
            midterm_percent=data.midterm_percent,
            final_percent=data.final_percent,
            status="active",
        )

        return self.subject_repository.create(
            subject=subject,
            university=university,
            department=department,
        )
