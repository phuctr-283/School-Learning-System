from apps.users.application.dto.user_dto import (
    CreateUserDTO,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)

from apps.users.domain.services.username_policy import (
    UsernamePolicy,
)

from apps.administrators.application.dto.school_admin.register_school_admin_dto import (
    RegisterSchoolAdminDTO,
)

from apps.administrators.domain.entities.school_admin_entity import (
    SchoolAdmin,
)


class RegisterSchoolAdminUseCase:

    def __init__(
        self,
        create_user_use_case,
        school_admin_repository,
        school_admin_id_generator,
        university_repository,
    ):

        self.create_user_use_case = create_user_use_case

        self.school_admin_repository = school_admin_repository

        self.school_admin_id_generator = school_admin_id_generator

        self.university_repository = university_repository

    def execute(
        self,
        data: RegisterSchoolAdminDTO,
    ):

        full_name = data.full_name.strip()

        username = UsernamePolicy.normalize(data.username)

        # =========================================
        # VALIDATE NAME
        # =========================================

        if not full_name:

            raise ValueError("Họ và tên không được để trống")

        # =========================================
        # EXTRACT UNIVERSITY DOMAIN
        # =========================================

        university_domain = UsernamePolicy.extract_school_domain(username)

        if not university_domain:

            raise ValueError("Username School Admin phải có dạng @admin.{domain}")

        # =========================================
        # FIND UNIVERSITY
        # =========================================

        university = self.university_repository.find_by_domain(university_domain)

        if not university:

            raise ValueError("Không tìm thấy trường đại học với domain này")

        # =========================================
        # VALIDATE DOMAIN
        # =========================================

        if not UsernamePolicy.validate_school_admin(
            username,
            university.domain,
        ):

            raise ValueError("Username không thuộc domain quản trị của trường")

        # =========================================
        # CHECK ADMIN EMAIL
        # =========================================

        if self.school_admin_repository.find_by_email(username):

            raise ValueError("Email School Admin đã tồn tại")

        # =========================================
        # GENERATE SCHOOL ADMIN ID
        # =========================================

        school_admin_id = self.school_admin_id_generator.generate(
            university.university_id
        )

        # =========================================
        # CREATE LOGIN ACCOUNT
        # =========================================

        self.create_user_use_case.execute(
            CreateUserDTO(
                username=username,
                password=data.password,
                account_level=AccountLevel.SCHOOL_ADMIN,
                university_id=university.university_id,
            )
        )

        # =========================================
        # CREATE ADMIN PROFILE
        # =========================================

        admin = SchoolAdmin(
            school_admin_id=school_admin_id,
            full_name=full_name,
            gender=None,
            email=username,
            phone=None,
            university_id=university.university_id,
            university_name=university.name,
            status="active",
        )

        self.school_admin_repository.create(admin)

        return admin
