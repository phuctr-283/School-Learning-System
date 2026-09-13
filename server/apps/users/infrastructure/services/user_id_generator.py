import re

from apps.users.domain.enums.account_level import (
    AccountLevel,
)

from apps.users.infrastructure.persistence.models.user_model import (
    UserModel,
)


class UserIdGenerator:

    # =========================================
    # CONFIG
    # =========================================

    SUPER_ADMIN_PREFIX = "SA"

    SEQUENCE_LENGTH = 8

    # =========================================
    # GENERATE
    # =========================================

    def generate(
        self,
        account_level: AccountLevel,
        university_id=None,
    ) -> str:

        if not isinstance(
            account_level,
            AccountLevel,
        ):
            raise ValueError("Account level không hợp lệ")

        if account_level == AccountLevel.SUPER_ADMIN:
            return self._generate_super_admin_id()

        if not university_id:
            raise ValueError("Tài khoản phải có university_id")

        university_id = str(university_id).strip().lower()

        if not university_id:
            raise ValueError("University ID không được để trống")

        return self._generate_university_id(
            university_id=university_id,
            account_level=account_level,
        )

    def _generate_super_admin_id(self):

        prefix = self.SUPER_ADMIN_PREFIX

        pattern = rf"^{prefix}(\d+)$"

        users = UserModel.objects(user_id__regex=pattern)

        max_sequence = 0

        for user in users:

            match = re.match(
                pattern,
                user.user_id,
            )

            if not match:
                continue

            sequence = int(match.group(1))

            if sequence > max_sequence:
                max_sequence = sequence

        next_sequence = max_sequence + 1

        return f"{prefix}" f"{next_sequence:05d}"

    # =========================================
    # UNIVERSITY USER ID
    # =========================================

    def _generate_university_id(
        self,
        university_id: str,
        account_level: AccountLevel,
    ):

        level = account_level.value

        prefix = f"{university_id}" f"{level}"

        pattern = rf"^{re.escape(prefix)}(\d+)$"

        users = UserModel.objects(user_id__regex=pattern)

        max_sequence = 0

        for user in users:

            match = re.match(
                pattern,
                user.user_id,
            )

            if not match:
                continue

            sequence = int(match.group(1))

            if sequence > max_sequence:
                max_sequence = sequence

        next_sequence = max_sequence + 1

        return f"{prefix}" f"{next_sequence:0{self.SEQUENCE_LENGTH}d}"
