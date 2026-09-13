import re

from apps.administrators.infrastructure.persistence.models.school_admin_model import (
    SchoolAdminModel,
)


class SchoolAdminIdGenerator:

    SEQUENCE_LENGTH = 5

    def generate(
        self,
        university_id: str,
    ) -> str:

        university_id = str(university_id).strip().upper()

        if not university_id:
            raise ValueError("University ID không được để trống")

        pattern = rf"^{re.escape(university_id)}(\d+)$"

        admins = SchoolAdminModel.objects(school_admin_id__regex=pattern)

        max_sequence = 0

        for admin in admins:

            match = re.match(
                pattern,
                admin.school_admin_id,
            )

            if not match:
                continue

            sequence = int(match.group(1))

            if sequence > max_sequence:
                max_sequence = sequence

        next_sequence = max_sequence + 1

        return f"{university_id}" f"{next_sequence:0{self.SEQUENCE_LENGTH}d}"
