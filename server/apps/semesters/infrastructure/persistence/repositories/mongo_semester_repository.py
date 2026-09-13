from apps.semesters.domain.repositories.semester_repository import (
    SemesterRepository,
)

from apps.semesters.domain.entities.semester_entity import (
    Semester,
)

from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)

from apps.academic_years.infrastructure.persistence.models.academic_year_model import (
    AcademicYearModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoSemesterRepository(SemesterRepository):

    # =========================================================
    # PRIVATE
    # =========================================================

    def _to_entity(
        self,
        semester_model: SemesterModel,
    ):

        if not semester_model:
            return None

        academic_year = semester_model.academic_year

        if not academic_year:
            return None

        university = academic_year.university

        if not university:
            return None

        return Semester(
            semester_id=semester_model.semester_id,
            name=semester_model.name,
            semester_number=(semester_model.semester_number),
            academic_year_id=(academic_year.academic_year_id),
            academic_year_name=(academic_year.name),
            university_id=(university.university_id),
            university_name=(university.name),
            start_date=(semester_model.start_date),
            end_date=(semester_model.end_date),
            status=(semester_model.status),
        )

    # =========================================================
    # GET ALL SEMESTERS BY UNIVERSITY
    # =========================================================

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        academic_years = list(
            AcademicYearModel.objects(
                university=university,
            )
        )

        if not academic_years:
            return []

        semesters = SemesterModel.objects(
            academic_year__in=academic_years,
        ).order_by(
            "-academic_year",
            "semester_number",
        )

        return [self._to_entity(semester) for semester in semesters]

    # =========================================================
    # GET ACTIVE / PLANNED SEMESTERS
    # =========================================================

    def get_active_planned(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        academic_years = list(
            AcademicYearModel.objects(
                university=university,
            )
        )

        if not academic_years:
            return []

        semesters = SemesterModel.objects(
            academic_year__in=academic_years,
            status__in=[
                "active",
                "planned",
            ],
        ).order_by(
            "-academic_year",
            "semester_number",
        )

        return [self._to_entity(semester) for semester in semesters]

    # =========================================================
    # GET SEMESTER BY ID
    # =========================================================

    def get_by_id(
        self,
        university_id: str,
        semester_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        academic_years = AcademicYearModel.objects(
            university=university,
        )

        semester = SemesterModel.objects(
            semester_id=semester_id,
            academic_year__in=academic_years,
        ).first()

        if not semester:
            return None

        return self._to_entity(semester)

    # =========================================================
    # GET SEMESTER BY NAME
    # =========================================================

    def get_by_name(
        self,
        university_id: str,
        academic_year_id: str,
        name: str,
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

        semester = SemesterModel.objects(
            academic_year=academic_year,
            name=name,
        ).first()

        if not semester:
            return None

        return self._to_entity(semester)

    # =========================================================
    # GET BY ACADEMIC YEAR + SEMESTER NUMBER
    # =========================================================

    def get_by_academic_year_and_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
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

        semester = SemesterModel.objects(
            academic_year=academic_year,
            semester_number=semester_number,
        ).first()

        if not semester:
            return None

        return self._to_entity(semester)

    def get_by_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            return None

        return SemesterModel.objects(
            semester_number=semester_number,
            academic_year=academic_year,
        ).first()

    # =========================================================
    # EXISTS BY SEMESTER NUMBER
    # =========================================================

    def exists_by_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        academic_year = AcademicYearModel.objects(
            university=university,
            academic_year_id=academic_year_id,
        ).first()

        if not academic_year:
            return False

        return (
            SemesterModel.objects(
                academic_year=academic_year,
                semester_number=semester_number,
            ).first()
            is not None
        )

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    def update_status(
        self,
        university_id: str,
        semester_id: str,
        status: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        academic_years = AcademicYearModel.objects(
            university=university,
        )

        semester_model = SemesterModel.objects(
            semester_id=semester_id,
            academic_year__in=academic_years,
        ).first()

        if not semester_model:
            return None

        semester_model.status = status

        semester_model.save(
            validate=False,
        )

        return self._to_entity(semester_model)

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        semester,
        academic_year,
    ):

        semester_model = SemesterModel(
            semester_id=semester.semester_id,
            name=semester.name,
            semester_number=(semester.semester_number),
            academic_year=academic_year,
            start_date=semester.start_date,
            end_date=semester.end_date,
            status=semester.status,
        )

        semester_model.save()

        return self._to_entity(semester_model)
