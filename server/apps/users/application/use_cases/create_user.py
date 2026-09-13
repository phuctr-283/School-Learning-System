from django.utils import timezone

from apps.users.application.dto.user_dto import (
    CreateUserDTO,
)

from apps.users.domain.entities.user_entity import (
    UserAccount,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class CreateUserUseCase:

    def __init__(
        self,
        user_repository,
        password_service,
        user_id_generator,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.user_id_generator = user_id_generator

    def execute(
        self,
        data: CreateUserDTO,
    ) -> UserAccount:

        username = data.username.strip().lower()

        if not username:
            raise ValueError("Username không được để trống")

        if not data.password:
            raise ValueError("Password không được để trống")

        if len(data.password) < 8:
            raise ValueError("Password phải có ít nhất 8 ký tự")

        if not isinstance(
            data.account_level,
            AccountLevel,
        ):
            raise ValueError("Account level không hợp lệ")

        if data.account_level == AccountLevel.SUPER_ADMIN:

            if data.university_id:
                raise ValueError("Super Admin không thuộc trường")

        else:

            if not data.university_id:
                raise ValueError("Tài khoản phải thuộc một trường")

        existing_user = self.user_repository.find_by_username(username)

        if existing_user:
            raise ValueError("Username đã tồn tại")

        if data.user_id:

            user_id = data.user_id

        else:

            user_id = self.user_id_generator.generate(
                account_level=data.account_level,
                university_id=data.university_id,
            )

        now = timezone.now()

        user = UserAccount(
            user_id=user_id,
            username=username,
            password=self.password_service.hash(data.password),
            account_level=data.account_level,
            university_id=data.university_id,
            last_login=None,
            is_login=False,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return self.user_repository.create(user)
