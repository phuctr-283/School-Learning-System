from apps.academic_years.domain.repositories.academic_year_repository import (
    AcademicYearRepository,
)

from apps.academic_years.domain.entities.academic_year_entity import (
    AcademicYear,
)

from apps.academic_years.infrastructure.persistence.models.academic_year_model import (
    AcademicYearModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoAcademicYearRepository(AcademicYearRepository):
    def get_by_id(
        self,
        university_id: str,
        academic_year_id: str,
    ):

        if not university_id:
            return None

        if not academic_year_id:
            return None

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        academic_year = AcademicYearModel.objects(
            university=university,
            academic_year_id=academic_year_id,
        ).first()

        return academic_year

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        academic_years = AcademicYearModel.objects(
            university=university,
        ).order_by("-start_date")

        return [
            AcademicYear(
                academic_year_id=academic_year.academic_year_id,
                university_id=university.university_id,
                university_name=university.name,
                name=academic_year.name,
                start_date=academic_year.start_date,
                end_date=academic_year.end_date,
                status=academic_year.status,
            )
            for academic_year in academic_years
        ]

    def exists_by_name(
        self,
        university,
        name: str,
    ):

        return (
            AcademicYearModel.objects(
                university=university,
                name=name,
            ).first()
            is not None
        )

    def find_by_id(
        self,
        university_id: str,
    ):

        return UniversityModel.objects(
            university_id=university_id,
        ).first()

    def create(
        self,
        academic_year,
        university,
    ):

        academic_year_model = AcademicYearModel(
            academic_year_id=(academic_year.academic_year_id),
            university=university,
            name=academic_year.name,
            start_date=academic_year.start_date,
            end_date=academic_year.end_date,
            status=academic_year.status,
        )

        academic_year_model.save()

        return AcademicYear(
            academic_year_id=(academic_year_model.academic_year_id),
            university_id=university.university_id,
            university_name=university.name,
            name=academic_year_model.name,
            start_date=academic_year_model.start_date,
            end_date=academic_year_model.end_date,
            status=academic_year_model.status,
        )

    def update_status(
        self,
        university_id: str,
        academic_year_id: str,
        status: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        academic_year = AcademicYearModel.objects(
            university=university,
            academic_year_id=academic_year_id,
        ).first()

        if not academic_year:
            return None

        academic_year.status = status

        academic_year.save(
            validate=False,
        )

        return AcademicYear(
            academic_year_id=academic_year.academic_year_id,
            university_id=university.university_id,
            university_name=university.name,
            name=academic_year.name,
            start_date=academic_year.start_date,
            end_date=academic_year.end_date,
            status=academic_year.status,
        )

    def get_active_and_planned_by_university(self, university_id: str):
        university = UniversityModel.objects(university_id=university_id).first()

        if not university:
            return []

        academic_years = AcademicYearModel.objects(
            university=university,
            status__in=["active", "planned"],
        ).order_by("-start_date")

        return [
            AcademicYear(
                academic_year_id=academic_year.academic_year_id,
                university_id=university.university_id,
                university_name=university.name,
                name=academic_year.name,
                start_date=academic_year.start_date,
                end_date=academic_year.end_date,
                status=academic_year.status,
            )
            for academic_year in academic_years
        ]

    def get_academic_year_by_id(
        self,
        university_id: str,
        academic_year_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        return AcademicYearModel.objects(
            university=university,
            academic_year_id=academic_year_id,
        ).first()

    def get_by_name(
        self,
        university_id: str,
        name: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        return AcademicYearModel.objects(
            university=university,
            name=name,
        ).first()
