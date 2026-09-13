from apps.lessons.domain.entities.semester_lesson_plan_entity import (
    SemesterLessonPlan,
)

from apps.lessons.domain.repositories.semester_lesson_plan_repository import (
    SemesterLessonPlanRepository,
)

from apps.lessons.infrastructure.persistence.models.semester_lesson_plan_model import (
    SemesterLessonPlanModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)

from apps.academic_years.infrastructure.persistence.models.academic_year_model import (
    AcademicYearModel,
)


class MongoSemesterLessonPlanRepository(SemesterLessonPlanRepository):

    # =========================================================
    # PRIVATE
    # =========================================================

    def _to_entity(
        self,
        model,
    ):

        if not model:
            return None

        semester = model.semester

        if not semester:
            return None

        academic_year = semester.academic_year

        if not academic_year:
            return None

        university = model.university

        if not university:
            return None

        return SemesterLessonPlan(
            semester_lesson_plan_id=model.semester_lesson_plan_id,
            university_id=university.university_id,
            semester_id=semester.semester_id,
            academic_year_id=academic_year.academic_year_id,
            academic_year_name=academic_year.name,
            semester_number=semester.semester_number,
            semester_name=semester.name,
            total_lessons=model.total_lessons,
        )

    # =========================================================
    # GET BY UNIVERSITY
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

        models = list(
            SemesterLessonPlanModel.objects(
                university=university,
            )
        )

        return [self._to_entity(model) for model in models]

    # =========================================================
    # GET ALL
    # =========================================================

    def get_all(
        self,
        university_id: str,
    ):

        return self.get_by_university(university_id)

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        university_id: str,
        semester_lesson_plan_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        model = SemesterLessonPlanModel.objects(
            university=university,
            semester_lesson_plan_id=semester_lesson_plan_id,
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    # =========================================================
    # GET BY SEMESTER
    # =========================================================

    def get_by_semester(
        self,
        university_id: str,
        semester_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        semester = SemesterModel.objects(
            semester_id=semester_id,
        ).first()

        if not semester:
            return None

        academic_year = semester.academic_year

        if not academic_year:
            return None

        if academic_year.university != university:
            return None

        model = SemesterLessonPlanModel.objects(
            university=university,
            semester=semester,
        ).first()

        if not model:
            return None

        return self._to_entity(model)

    # =========================================================
    # EXISTS BY SEMESTER
    # =========================================================

    def exists_by_semester(
        self,
        university_id: str,
        semester_id: str,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        semester = SemesterModel.objects(
            semester_id=semester_id,
        ).first()

        if not semester:
            return False

        academic_year = semester.academic_year

        if not academic_year:
            return False

        if academic_year.university != university:
            return False

        model = SemesterLessonPlanModel.objects(
            university=university,
            semester=semester,
        ).first()

        return model is not None

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        entity: SemesterLessonPlan,
        university_id: str,
        academic_year_id: str,
    ) -> SemesterLessonPlan:

        # -----------------------------------------------------
        # UNIVERSITY
        # -----------------------------------------------------

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        # -----------------------------------------------------
        # ACADEMIC YEAR
        # -----------------------------------------------------

        academic_year = AcademicYearModel.objects(
            academic_year_id=academic_year_id,
            university=university,
        ).first()

        if not academic_year:
            raise ValueError("Không tìm thấy năm học.")

        # -----------------------------------------------------
        # SEMESTER
        # -----------------------------------------------------

        semester_model = SemesterModel.objects(
            semester_id=entity.semester_id,
            academic_year=academic_year,
        ).first()

        if not semester_model:
            raise ValueError("Không tìm thấy học kỳ.")

        # -----------------------------------------------------
        # CREATE
        # -----------------------------------------------------

        model = SemesterLessonPlanModel(
            semester_lesson_plan_id=(entity.semester_lesson_plan_id),
            university=university,
            semester=semester_model,
            total_lessons=entity.total_lessons,
        )

        model.save()

        return self._to_entity(model)
