from django.utils import timezone

from apps.universities.application.dto.create_university_dto import (
    CreateUniversityDTO,
)

from apps.universities.domain.entities.university_entity import (
    University,
)


class CreateUniversityUseCase:

    def __init__(
        self,
        university_repository,
    ):
        self.university_repository = (
            university_repository
        )

    def execute(
        self,
        data: CreateUniversityDTO,
    ):

        university_id = data.university_id.strip()
        name = data.name.strip()
        domain = data.domain.strip().lower()
        email = data.email.strip().lower()
        phone = data.phone.strip()

        # =========================================
        # VALIDATE UNIVERSITY ID
        # =========================================

        if not university_id:
            raise ValueError(
                "Mã trường không được để trống"
            )

        if len(university_id) > 50:
            raise ValueError(
                "Mã trường không được vượt quá 50 ký tự"
            )

        # =========================================
        # VALIDATE NAME
        # =========================================

        if not name:
            raise ValueError(
                "Tên trường không được để trống"
            )

        if len(name) > 200:
            raise ValueError(
                "Tên trường không được vượt quá 200 ký tự"
            )

        # =========================================
        # VALIDATE DOMAIN
        # =========================================

        if not domain:
            raise ValueError(
                "Domain không được để trống"
            )

        if len(domain) > 100:
            raise ValueError(
                "Domain không được vượt quá 100 ký tự"
            )

        # =========================================
        # VALIDATE EMAIL
        # =========================================

        if not email:
            raise ValueError(
                "Email không được để trống"
            )

        # =========================================
        # VALIDATE PHONE
        # =========================================

        if not phone:
            raise ValueError(
                "Số điện thoại không được để trống"
            )

        # =========================================
        # CHECK DUPLICATE
        # =========================================

        if self.university_repository.find_by_id(
            university_id
        ):
            raise ValueError(
                "Mã trường đã tồn tại"
            )

        if self.university_repository.exists_by_name(
            name
        ):
            raise ValueError(
                "Tên trường đã tồn tại"
            )

        if self.university_repository.exists_by_domain(
            domain
        ):
            raise ValueError(
                "Domain đã tồn tại"
            )

        if self.university_repository.exists_by_email(
            email
        ):
            raise ValueError(
                "Email đã tồn tại"
            )

        # =========================================
        # CREATE
        # =========================================

        now = timezone.now()

        university = University(
            university_id=university_id,
            name=name,
            domain=domain,
            email=email,
            phone=phone,
            is_active=True,
            updated_at=now,
        )

        return self.university_repository.create(
            university
        )