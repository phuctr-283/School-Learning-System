class UsernamePolicy:

    SUPER_ADMIN_DOMAIN = "admin.vn"
    SCHOOL_ADMIN_PREFIX = "admin."
    STUDENT_PREFIX = "student."

    @staticmethod
    def normalize(username: str) -> str:
        return username.strip().lower()

    # =========================================================
    # SUPER ADMIN
    # =========================================================

    @classmethod
    def validate_super_admin(cls, username: str) -> bool:

        username = cls.normalize(username)

        return username.endswith(f"@{cls.SUPER_ADMIN_DOMAIN}")

    # =========================================================
    # SCHOOL ADMIN
    # =========================================================

    @classmethod
    def extract_school_domain(
        cls,
        username: str,
    ) -> str | None:

        username = cls.normalize(username)

        if "@" not in username:
            return None

        domain = username.split("@", 1)[1]

        if not domain.startswith(cls.SCHOOL_ADMIN_PREFIX):
            return None

        university_domain = domain[len(cls.SCHOOL_ADMIN_PREFIX) :]

        return university_domain or None

    @classmethod
    def validate_school_admin(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)

        university_domain = university_domain.strip().lower()

        return username.endswith(f"@admin.{university_domain}")

    # =========================================================
    # TEACHER
    # =========================================================

    @classmethod
    def validate_teacher(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)

        university_domain = university_domain.strip().lower()

        return username.endswith(f"@{university_domain}")

    # =========================================================
    # STUDENT
    # =========================================================

    @classmethod
    def validate_student(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)

        university_domain = university_domain.strip().lower()

        return username.endswith(f"@student.{university_domain}")

    # =========================================================
    # ACCOUNT TYPE
    # =========================================================

    @classmethod
    def get_account_type(
        cls,
        username: str,
        university_domain: str,
    ) -> str | None:

        username = cls.normalize(username)
        university_domain = university_domain.strip().lower()

        if cls.validate_super_admin(username):
            return "super_admin"

        if cls.validate_school_admin(
            username,
            university_domain,
        ):
            return "school_admin"

        if cls.validate_student(
            username,
            university_domain,
        ):
            return "student"

        if cls.validate_teacher(
            username,
            university_domain,
        ):
            return "teacher"

        return None


class UsernamePolicy:

    SUPER_ADMIN_DOMAIN = "admin.vn"
    SCHOOL_ADMIN_PREFIX = "admin."
    STUDENT_PREFIX = "student."

    @staticmethod
    def normalize(username: str) -> str:
        return username.strip().lower()

    # =========================================================
    # SUPER ADMIN
    # =========================================================

    @classmethod
    def validate_super_admin(cls, username: str) -> bool:

        username = cls.normalize(username)

        return username.endswith(f"@{cls.SUPER_ADMIN_DOMAIN}")

    # =========================================================
    # SCHOOL ADMIN
    # =========================================================

    @classmethod
    def extract_school_domain(
        cls,
        username: str,
    ) -> str | None:

        username = cls.normalize(username)

        if "@" not in username:
            return None

        domain = username.split("@", 1)[1]

        if not domain.startswith(cls.SCHOOL_ADMIN_PREFIX):
            return None

        university_domain = domain[len(cls.SCHOOL_ADMIN_PREFIX) :]

        return university_domain or None

    @classmethod
    def validate_school_admin(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)
        university_domain = university_domain.strip().lower()

        return username.endswith(f"@admin.{university_domain}")

    # =========================================================
    # TEACHER
    # =========================================================

    @classmethod
    def validate_teacher(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)
        university_domain = university_domain.strip().lower()

        return username.endswith(f"@{university_domain}")

    # =========================================================
    # STUDENT
    # =========================================================

    @classmethod
    def validate_student(
        cls,
        username: str,
        university_domain: str,
    ) -> bool:

        username = cls.normalize(username)
        university_domain = university_domain.strip().lower()

        return username.endswith(f"@student.{university_domain}")

    # =========================================================
    # ACCOUNT TYPE
    # =========================================================

    @classmethod
    def get_account_type(
        cls,
        username: str,
        university_domain: str | None = None,
    ) -> str | None:

        username = cls.normalize(username)

        if cls.validate_super_admin(username):
            return "super_admin"

        if university_domain:

            university_domain = university_domain.strip().lower()

            if cls.validate_school_admin(
                username,
                university_domain,
            ):
                return "school_admin"

            if cls.validate_student(
                username,
                university_domain,
            ):
                return "student"

            if cls.validate_teacher(
                username,
                university_domain,
            ):
                return "teacher"

        return None
