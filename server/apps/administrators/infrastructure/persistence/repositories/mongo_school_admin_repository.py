from apps.administrators.domain.entities.school_admin_entity import (
    SchoolAdmin,
)

from apps.administrators.infrastructure.persistence.models.school_admin_model import (
    SchoolAdminModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoSchoolAdminRepository:

    def get_all(self):

        models = SchoolAdminModel.objects.order_by("-school_admin_id").select_related()

        return [
            SchoolAdmin(
                school_admin_id=model.school_admin_id,
                full_name=model.full_name,
                gender=model.gender,
                email=model.email,
                phone=model.phone,
                university_id=(
                    model.university.university_id if model.university else None
                ),
                university_name=(model.university.name if model.university else None),
                status=model.status,
            )
            for model in models
        ]

    def create(self, entity: SchoolAdmin):

        university = UniversityModel.objects(university_id=entity.university_id).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học")

        model = SchoolAdminModel(
            school_admin_id=entity.school_admin_id,
            full_name=entity.full_name,
            gender=entity.gender,
            email=entity.email,
            phone=entity.phone,
            university=university,
            status=entity.status,
        )

        model.save()

        return model

    def find_by_email(self, email):

        return SchoolAdminModel.objects(email=email).first()
