from apps.users.application.use_cases.logout_user import (
    LogoutUserUseCase,
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


def logout_use_case() -> LogoutUserUseCase:

    return LogoutUserUseCase(
        jwt_service=JWTService(),
        revoked_token_repository=RevokedTokenRepository(),
        user_repository=MongoUserRepository(),
    )