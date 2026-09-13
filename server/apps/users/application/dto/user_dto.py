from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from apps.users.domain.enums.account_level import AccountLevel


@dataclass
class CreateUserDTO:

    username: str
    password: str
    account_level: AccountLevel
    university_id: Optional[str] = None
    user_id: Optional[str] = None

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