from abc import ABC, abstractmethod
from typing import Optional

from apps.users.domain.entities.user_entity import (
    UserAccount,
)


class UserRepository(ABC):

    @abstractmethod
    def find_by_id(
        self,
        user_id: str,
    ) -> Optional[UserAccount]:
        raise NotImplementedError

    @abstractmethod
    def find_by_username(
        self,
        username: str,
    ) -> Optional[UserAccount]:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        user: UserAccount,
    ) -> UserAccount:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        user: UserAccount,
    ) -> UserAccount:
        raise NotImplementedError