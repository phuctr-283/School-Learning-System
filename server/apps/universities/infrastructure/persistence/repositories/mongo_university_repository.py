import time
from apps.universities.domain.repositories.university_repository import (
    UniversityRepository,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoUniversityRepository(UniversityRepository):

    def create(self, university):

        model = UniversityModel(
            university_id=university.university_id,
            name=university.name,
            domain=university.domain,
            email=university.email,
            phone=university.phone,
            is_active=university.is_active,
            updated_at=university.updated_at,
        )

        model.save()

        return university

    def find_by_id(self, university_id):

        return UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

    def find_by_name(self, name):

        return UniversityModel.objects(name=name).first()

    def find_by_domain(self, domain):

        return UniversityModel.objects(domain=domain).first()

    def find_by_email(self, email):

        return UniversityModel.objects(email=email).first()

    def get_all(self):

        return list(UniversityModel.objects.order_by("name"))

    def get_active(self):

        start = time.time()

        print(">>> GET ACTIVE UNIVERSITIES: START")

        universities = list(UniversityModel.objects(is_active=True).order_by("name"))

        print(
            ">>> GET ACTIVE UNIVERSITIES:",
            time.time() - start,
            "seconds",
            "COUNT:",
            len(universities),
        )

        return universities

    def exists_by_name(self, name):

        return UniversityModel.objects(name=name).first() is not None

    def exists_by_domain(self, domain):

        return UniversityModel.objects(domain=domain).first() is not None

    def exists_by_email(self, email):

        return UniversityModel.objects(email=email).first() is not None

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        university_id: str,
    ):

        if not university_id:
            return None

        return (
            UniversityModel.objects(
                university_id=university_id,
                is_active = True,
            )
            .first()
        )