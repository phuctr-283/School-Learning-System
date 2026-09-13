from apps.departments.domain.entities.department_entity import (
    Department,
)


class CreateDepartmentUseCase:

    def __init__(
        self,
        department_repository,
        university_repository,
        teacher_repository,
    ):

        self.department_repository = department_repository

        self.university_repository = university_repository

        self.teacher_repository = teacher_repository

    def execute(
        self,
        data,
        university_id: str,
    ):

        department_id = data.department_id.strip().upper()
        department_number = data.department_number.strip()
        name = data.name.strip()
        head_id = data.head_id.strip() if data.head_id else None

        if not department_id:
            raise ValueError("Mã khoa không được để trống")

        if not department_number:
            raise ValueError("Số khoa không được để trống")

        if not name:
            raise ValueError("Tên khoa không được để trống")

        if not university_id:
            raise ValueError("Không xác định được trường đại học")

        university = self.university_repository.find_by_id(university_id)

        if not university:
            raise ValueError("Không tìm thấy trường đại học")

        existing_department = self.department_repository.find_by_id(department_id)

        if existing_department:
            raise ValueError("Mã khoa đã tồn tại")

        exists_number = self.department_repository.exists_department_number(
            university_id,
            department_number,
        )

        if exists_number:

            raise ValueError("Số khoa đã tồn tại trong trường")

        head = None

        if head_id:

            head = self.teacher_repository.find_by_id(head_id, department_id)

            if not head:

                raise ValueError("Không tìm thấy giảng viên")

            # Nếu Teacher có university_id

            if head.university_id != university_id:

                raise ValueError("Trưởng khoa phải thuộc cùng trường")

        # =========================================
        # CREATE ENTITY
        # =========================================

        department = Department(
            department_id=department_id,
            department_number=department_number,
            name=name,
            university_id=university.university_id,
            university_name=university.name,
            head_id=(head.teacher_id if head else None),
            head_name=(head.full_name if head else None),
            is_active=True,
        )

        # =========================================
        # SAVE
        # =========================================

        return self.department_repository.create(department)
