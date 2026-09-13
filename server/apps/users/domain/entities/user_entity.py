from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


@dataclass
class UserAccount:

    user_id: Optional[str]
    username: str
    password: str
    account_level: AccountLevel
    university_id: Optional[str]
    last_login: Optional[datetime] = None
    is_login: bool = False
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def login(
        self,
        login_time: datetime,
    ) -> None:

        self.last_login = login_time
        self.is_login = True

    def logout(self) -> None:
        self.is_login = False

    def is_super_admin(self) -> bool:
        return (
            self.account_level
            == AccountLevel.SUPER_ADMIN
        )

    def is_school_admin(self) -> bool:
        return (
            self.account_level
            == AccountLevel.SCHOOL_ADMIN
        )

    def is_teacher(self) -> bool:
        return (
            self.account_level
            == AccountLevel.TEACHER
        )

    def is_student(self) -> bool:
        return (
            self.account_level
            == AccountLevel.STUDENT
        )