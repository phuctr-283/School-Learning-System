from apps.users.application.use_cases.refresh_token import (
    RefreshTokenUseCase,
)

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.persistence.repositories.revoked_token_repository import (
    RevokedTokenRepository,
)

from apps.users.infrastructure.services.jwt_service import (
    JWTService,
)


def refresh_token_use_case() -> RefreshTokenUseCase:

    return RefreshTokenUseCase(
        user_repository=MongoUserRepository(),
        jwt_service=JWTService(),
        revoked_token_repository=RevokedTokenRepository(),
    )