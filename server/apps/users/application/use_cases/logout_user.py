from apps.users.application.dto.auth_dto import (
    LogoutDTO,
)


class LogoutUserUseCase:

    def __init__(
        self,
        jwt_service,
        revoked_token_repository,
        user_repository,
    ):

        self.jwt_service = jwt_service

        self.revoked_token_repository = revoked_token_repository

        self.user_repository = user_repository

    def execute(
        self,
        data: LogoutDTO,
    ):

        try:

            payload = self.jwt_service.decode_refresh_token(data.refresh_token)

        except Exception:

            raise ValueError("Refresh token không hợp lệ")

        jti = payload.get("jti")

        user_id = payload.get("user_id")

        if not jti:

            raise ValueError("Refresh token không có jti")

        if not user_id:

            raise ValueError("Refresh token không có user_id")

        if not (self.revoked_token_repository.exists(jti)):

            self.revoked_token_repository.revoke(
                jti=jti,
                user_id=user_id,
                expires_at=payload.get("exp"),
            )

        user = self.user_repository.find_by_id(user_id)

        if user and user.is_login:

            user.logout()

            self.user_repository.update(user)
