from abc import ABC, abstractmethod

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class UserIdGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        account_level: AccountLevel,
    ) -> str:
        raise NotImplementedError