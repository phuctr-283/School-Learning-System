from typing import Optional

from django.utils import timezone
from mongoengine.errors import ValidationError

from apps.users.domain.entities.user_entity import (
    UserAccount,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)

from apps.users.domain.repositories.user_repository import (
    UserRepository,
)

from apps.users.infrastructure.persistence.models.user_model import (
    UserModel,
)


class MongoUserRepository(UserRepository):

    def _to_entity(
        self,
        model: UserModel,
    ) -> UserAccount:

        return UserAccount(
            user_id=model.user_id,
            username=model.username,
            password=model.password,
            account_level=AccountLevel(model.account_level),
            university_id=model.university_id,
            last_login=model.last_login,
            is_login=model.is_login,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def find_by_id(
        self,
        user_id: str,
    ) -> Optional[UserAccount]:

        try:

            model = UserModel.objects(user_id=user_id).first()

        except ValidationError:

            return None

        if not model:

            return None

        return self._to_entity(model)

    def find_by_username(
        self,
        username: str,
    ) -> Optional[UserAccount]:

        model = UserModel.objects(username=username).first()

        if not model:

            return None

        return self._to_entity(model)

    def create(
        self,
        user: UserAccount,
    ) -> UserAccount:

        now = timezone.now()

        if not user.user_id:

            raise ValueError("User ID không được để trống")

        model = UserModel(
            user_id=user.user_id,
            username=user.username,
            password=user.password,
            account_level=(user.account_level.value),
            university_id=(user.university_id),
            last_login=user.last_login,
            is_login=user.is_login,
            is_active=user.is_active,
            created_at=(user.created_at or now),
            updated_at=(user.updated_at or now),
        )

        model.save()

        return self._to_entity(model)

    def update(
        self,
        user: UserAccount,
    ) -> UserAccount:

        if not user.user_id:

            raise ValueError("User ID không được để trống")

        model = UserModel.objects(user_id=user.user_id).first()

        if not model:

            raise ValueError("Không tìm thấy tài khoản")

        model.username = user.username

        model.password = user.password

        model.account_level = user.account_level.value

        model.university_id = user.university_id

        model.last_login = user.last_login

        model.is_login = user.is_login

        model.is_active = user.is_active

        model.updated_at = timezone.now()

        model.save()

        return self._to_entity(model)
