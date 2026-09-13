from dataclasses import dataclass
from typing import Optional

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


@dataclass
class LoginDTO:

    username: str
    password: str

@dataclass
class RefreshTokenDTO:

    refresh_token: str

@dataclass
class LogoutDTO:

    refresh_token: str

@dataclass
class AuthUserDTO:

    user_id: str
    username: str
    account_level: AccountLevel
    university_id: Optional[str] = None
    @property
    def is_authenticated(self):
        return True
