from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class AccountLevelService:

    @staticmethod
    def is_super_admin(
        account_level: AccountLevel,
    ) -> bool:

        return account_level == AccountLevel.SUPER_ADMIN

    @staticmethod
    def is_school_admin(
        account_level: AccountLevel,
    ) -> bool:

        return account_level == AccountLevel.SCHOOL_ADMIN

    @staticmethod
    def is_teacher(
        account_level: AccountLevel,
    ) -> bool:

        return account_level == AccountLevel.TEACHER

    @staticmethod
    def is_student(
        account_level: AccountLevel,
    ) -> bool:

        return account_level == AccountLevel.STUDENT

    @staticmethod
    def has_level(
        account_level: AccountLevel,
        allowed_levels: list[AccountLevel],
    ) -> bool:

        return account_level in allowed_levels

    @staticmethod
    def has_minimum_level(
        account_level: AccountLevel,
        minimum_level: AccountLevel,
    ) -> bool:

        return account_level <= minimum_level
