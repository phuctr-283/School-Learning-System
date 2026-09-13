from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.domain.enums.account_level import AccountLevel
from apps.users.domain.entities.user_entity import UserAccount

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.services.password_service import (
    PasswordService,
)

from apps.users.infrastructure.services.user_id_generator import (
    UserIdGenerator,
)


class Command(BaseCommand):

    help = "Create initial Super Admin"

    def handle(self, *args, **options):

        user_repository = MongoUserRepository()
        password_service = PasswordService()
        user_id_generator = UserIdGenerator()

        username = "superadmin"
        password = "12345678"

        existing_user = (
            user_repository.find_by_username(
                username
            )
        )

        if existing_user:
            self.stdout.write(
                self.style.WARNING(
                    "Super Admin đã tồn tại."
                )
            )
            return

        user_id = user_id_generator.generate(
            account_level=AccountLevel.SUPER_ADMIN,
            university_id=None,
        )

        now = timezone.now()

        user = UserAccount(
            user_id=user_id,
            username=username,
            password=password_service.hash(
                password
            ),
            account_level=AccountLevel.SUPER_ADMIN,
            university_id=None,
            last_login=None,
            is_login=False,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        user_repository.create(user)

        self.stdout.write(
            self.style.SUCCESS(
                "Tạo Super Admin thành công."
            )
        )

        self.stdout.write(
            f"User ID : {user_id}"
        )

        self.stdout.write(
            f"Username: {username}"
        )

        self.stdout.write(
            f"Password: {password}"
        )