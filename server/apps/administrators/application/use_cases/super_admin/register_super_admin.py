from django.utils import timezone

from apps.users.application.dto.user_dto import (
    CreateUserDTO,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)

from apps.users.domain.services.username_policy import (
    UsernamePolicy,
)

from apps.administrators.application.dto.super_admin.register_super_admin_dto import (
    RegisterSuperAdminDTO,
)

from apps.administrators.domain.entities.super_admin_entity import (
    SuperAdmin,
)


class RegisterSuperAdminUseCase:

    def __init__(
        self,
        create_user_use_case,
        super_admin_repository,
        super_admin_id_generator,
    ):

        self.create_user_use_case = create_user_use_case

        self.super_admin_repository = super_admin_repository

        self.super_admin_id_generator = super_admin_id_generator

    def execute(
        self,
        data: RegisterSuperAdminDTO,
    ):

        full_name = data.full_name.strip()
        username = UsernamePolicy.normalize(data.username)

        if not full_name:
            raise ValueError("Họ và tên không được để trống")

        if not UsernamePolicy.validate_super_admin(username):
            raise ValueError("Super Admin phải sử dụng username có dạng @admin.vn")

        if self.super_admin_repository.find_by_email(username):
            raise ValueError("Email Super Admin đã tồn tại")

        # =========================================
        # GENERATE ADMIN ID
        # =========================================

        super_admin_id = self.super_admin_id_generator.generate()

        # =========================================
        # CREATE USER
        # =========================================

        user = self.create_user_use_case.execute(
            CreateUserDTO(
                username=username,
                password=data.password,
                account_level=AccountLevel.SUPER_ADMIN,
                university_id=None,
                user_id=super_admin_id,
            )
        )

        # =========================================
        # CREATE SUPER ADMIN PROFILE
        # =========================================

        admin = SuperAdmin(
            super_admin_id=super_admin_id,
            full_name=full_name,
            email=username,
            gender=None,
            phone=None,
            status="active",
        )

        self.super_admin_repository.create(admin)

        return admin
