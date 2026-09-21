from datetime import datetime
from uuid import uuid4

from django.contrib.auth.hashers import make_password

from apps.teachers.domain.entities.teacher_entity import (
    Teacher,
)

from apps.teachers.application.dto.register_teacher_dto import (
    RegisterTeacherDTO,
)

from apps.users.infrastructure.persistence.models.user_model import (
    UserModel,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class RegisterTeacherUseCase:

    def __init__(
        self,
        teacher_repository,
        university_repository,
        department_repository,
    ):

        self.teacher_repository = teacher_repository
        self.university_repository = university_repository
        self.department_repository = department_repository

    def execute(
        self,
        dto: RegisterTeacherDTO,
    ):

        # =========================================
        # NORMALIZE
        # =========================================

        full_name = dto.full_name.strip()
        university_id = dto.university_id.strip().upper()
        department_id = dto.department_id.strip().upper()
        email = dto.email.strip().lower()
        password = dto.password

        # =========================================
        # VALIDATE BASIC DATA
        # =========================================

        if not full_name:
            raise ValueError(
                "Họ và tên không được để trống"
            )

        if not university_id:
            raise ValueError(
                "Chưa chọn trường đại học"
            )

        if not department_id:
            raise ValueError(
                "Chưa chọn khoa"
            )

        if not email:
            raise ValueError(
                "Email không được để trống"
            )

        if not password:
            raise ValueError(
                "Mật khẩu không được để trống"
            )

        # =========================================
        # CHECK EMAIL IN USER ACCOUNT
        # =========================================

        existing_user = UserModel.objects(
            username=email,
        ).first()

        if existing_user:
            raise ValueError(
                "Email đã được sử dụng"
            )

        # =========================================
        # CHECK UNIVERSITY
        # =========================================

        university = (
            self.university_repository.find_by_id(
                university_id,
            )
        )

        if not university:
            raise ValueError(
                "Không tìm thấy trường đại học"
            )

        if not university.is_active:
            raise ValueError(
                "Trường đại học đang bị khóa"
            )

        # =========================================
        # CHECK DEPARTMENT
        # =========================================

        department = (
            self.department_repository.find_by_id(
                department_id,
                university_id,
            )
        )

        if not department:
            raise ValueError(
                "Không tìm thấy khoa"
            )

        if not department.is_active:
            raise ValueError(
                "Khoa đang bị khóa"
            )

        # =========================================
        # CHECK DEPARTMENT BELONGS TO UNIVERSITY
        # =========================================

        if (
            department.university.university_id
            != university_id
        ):
            raise ValueError(
                "Khoa không thuộc trường đại học đã chọn"
            )

        # =========================================
        # GENERATE TEACHER ID IN DEPARTMENT
        # =========================================

        teacher_id = self._generate_teacher_id(
            department,
        )

        # =========================================
        # CREATE USER ACCOUNT
        # =========================================

        now = datetime.utcnow()

        user = UserModel(
            user_id=f"GV-{uuid4().hex[:8].upper()}",
            username=email,
            password=make_password(password),
            account_level=AccountLevel.TEACHER.value,
            university_id=university_id,
            last_login=None,
            is_login=False,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        user.save()

        # =========================================
        # CREATE TEACHER DOMAIN ENTITY
        # =========================================

        teacher = Teacher(
            teacher_id=teacher_id,
            full_name=full_name,
            gender=None,
            date_of_birth=None,
            email=email,
            phone=None,
            department_id=department.department_id,
            department_name=department.name,
            university_id=university.university_id,
            university_name=university.name,
            status="active",
        )

        # =========================================
        # SAVE TEACHER
        # =========================================

        return self.teacher_repository.create(
            teacher,
            department,
        )

    # =========================================
    # GENERATE ID UNIQUE IN DEPARTMENT
    # =========================================

    def _generate_teacher_id(
        self,
        department,
    ) -> str:

        department_number = str(
            department.department_number
        )

        prefix = f"GV{department_number}"

        teachers = (
            self.teacher_repository.get_by_department(
                department,
            )
        )

        max_number = 0

        for teacher in teachers:

            teacher_id = teacher.teacher_id

            if not teacher_id.startswith(prefix):
                continue

            suffix = teacher_id[
                len(prefix):
            ]

            try:
                number = int(suffix)

            except ValueError:
                continue

            max_number = max(
                max_number,
                number,
            )

        return (
            f"{prefix}{max_number + 1:04d}"
        )