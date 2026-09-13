from django.contrib.auth.hashers import (
    make_password,
    check_password,
)

from apps.users.domain.services.password_service import (
    PasswordService as PasswordServiceInterface,
)


class PasswordService(
    PasswordServiceInterface
):

    def hash(
        self,
        password: str,
    ) -> str:

        return make_password(password)

    def verify(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:

        return check_password(
            password,
            hashed_password,
        )