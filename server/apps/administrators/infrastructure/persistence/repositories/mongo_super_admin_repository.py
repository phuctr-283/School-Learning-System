from apps.administrators.domain.repositories.super_admin_repository import (
    SuperAdminRepository,
)

from apps.administrators.infrastructure.persistence.models.super_admin_model import (
    SuperAdminModel,
)

from apps.administrators.domain.entities.super_admin_entity import (
    SuperAdmin,
)


class MongoSuperAdminRepository(SuperAdminRepository):

    def create(self, admin: SuperAdmin):

        model = SuperAdminModel(
            super_admin_id=admin.super_admin_id,
            full_name=admin.full_name,
            email=admin.email,
            gender=admin.gender,
            phone=admin.phone,
            status=admin.status,
        )

        model.save()

        return admin

    def find_by_email(self, email):

        return SuperAdminModel.objects(email=email).first()

    def get_all(self):

        return list(
            SuperAdminModel.objects(status="active").order_by("-super_admin_id")
        )
