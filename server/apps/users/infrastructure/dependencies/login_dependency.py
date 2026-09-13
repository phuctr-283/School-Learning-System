from apps.users.application.use_cases.login_user import (
    LoginUserUseCase,
)

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.services.jwt_service import (
    JWTService,
)

from apps.users.infrastructure.services.password_service import (
    PasswordService,
)


def login_use_case() -> LoginUserUseCase:

    return LoginUserUseCase(
        user_repository=MongoUserRepository(),
        jwt_service=JWTService(),
        password_service=PasswordService(),
    )