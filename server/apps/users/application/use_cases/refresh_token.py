from datetime import (
    datetime,
    timezone,
)

from apps.users.application.dto.auth_dto import (
    RefreshTokenDTO,
)


class RefreshTokenUseCase:

    def __init__(
        self,
        user_repository,
        jwt_service,
        revoked_token_repository,
    ):

        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.revoked_token_repository = revoked_token_repository

    def execute(
        self,
        data: RefreshTokenDTO,
    ):

        try:
            payload = self.jwt_service.decode_refresh_token(data.refresh_token)
        except Exception:
            raise ValueError("Refresh token không hợp lệ hoặc đã hết hạn")
        jti = payload.get("jti")
        if not jti:
            raise ValueError("Refresh token không có jti")
        if self.revoked_token_repository.exists(jti):
            raise ValueError("Refresh token đã bị thu hồi")
        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("Refresh token không có user_id")
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("Người dùng không tồn tại")
        if not user.is_active:
            raise ValueError("Tài khoản đã bị khóa")
        expires_at = datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc,
        )
        self.revoked_token_repository.revoke(
            jti=jti,
            user_id=user.user_id,
            expires_at=expires_at,
        )
        if not user.is_login:
            user.login(datetime.now(timezone.utc))
            user = self.user_repository.update(user)
        return self.jwt_service.generate_tokens(user)
