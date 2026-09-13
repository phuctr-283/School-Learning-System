from datetime import datetime, timezone

from apps.users.infrastructure.persistence.models.revoked_token_model import (
    RevokedTokenModel,
)


class RevokedTokenRepository:

    def revoke(
        self,
        jti,
        user_id,
        expires_at,
    ):
        if isinstance(expires_at, (int, float)):
            expires_at = datetime.fromtimestamp(
                expires_at,
                tz=timezone.utc,
            )

        if self.exists(jti):
            return

        RevokedTokenModel(
            jti=jti,
            user_id=str(user_id),
            expires_at=expires_at,
            revoked_at=datetime.now(timezone.utc),
        ).save()

    def exists(self, jti):

        if not jti:
            return False

        return RevokedTokenModel.objects(jti=jti).first() is not None
