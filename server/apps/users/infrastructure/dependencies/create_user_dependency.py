from apps.users.application.use_cases.create_user import (
    CreateUserUseCase,
)

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.services.password_service import (
    PasswordService,
)

from apps.users.infrastructure.services.user_id_generator import (
    UserIdGenerator,
)


def create_user_use_case() -> CreateUserUseCase:

    return CreateUserUseCase(
        user_repository=MongoUserRepository(),
        password_service=PasswordService(),
        user_id_generator=UserIdGenerator(),
    )