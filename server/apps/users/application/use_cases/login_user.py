from datetime import datetime, timezone

from apps.users.application.dto.auth_dto import (
    LoginDTO,
)


class LoginUserUseCase:

    def __init__(
        self,
        user_repository,
        jwt_service,
        password_service,
    ):

        self.user_repository = (
            user_repository
        )

        self.jwt_service = (
            jwt_service
        )

        self.password_service = (
            password_service
        )

    def execute(
        self,
        data: LoginDTO,
    ):

        username = (
            data.username
            .strip()
            .lower()
        )

        user = (
            self.user_repository
            .find_by_username(
                username
            )
        )

        if not user:

            raise ValueError(
                "Username hoặc password không đúng"
            )

        if not user.is_active:

            raise ValueError(
                "Tài khoản đã bị khóa"
            )

        if not (
            self.password_service.verify(
                data.password,
                user.password,
            )
        ):

            raise ValueError(
                "Username hoặc password không đúng"
            )

        login_time = datetime.now(
            timezone.utc
        )

        user.login(login_time)

        user = (
            self.user_repository
            .update(user)
        )

        tokens = (
            self.jwt_service
            .generate_tokens(user)
        )

        return {
            "user": user,
            "tokens": tokens,
        }