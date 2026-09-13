import re

from apps.administrators.infrastructure.persistence.models.super_admin_model import (
    SuperAdminModel,
)


class SuperAdminIdGenerator:

    PREFIX = "SA"
    SEQUENCE_LENGTH = 5

    def generate(self) -> str:

        pattern = rf"^{self.PREFIX}(\d+)$"

        admins = SuperAdminModel.objects(super_admin_id__regex=pattern)

        max_sequence = 0

        for admin in admins:

            match = re.match(
                pattern,
                admin.super_admin_id,
            )

            if not match:
                continue

            sequence = int(match.group(1))

            if sequence > max_sequence:
                max_sequence = sequence

        next_sequence = max_sequence + 1

        return f"{self.PREFIX}" f"{next_sequence:0{self.SEQUENCE_LENGTH}d}"
