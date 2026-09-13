from apps.lessons.domain.entities.course_lesson_plan_entity import (
    CourseLessonPlan,
)

from apps.lessons.domain.repositories.course_lesson_plan_repository import (
    CourseLessonPlanRepository,
)

from apps.lessons.infrastructure.persistence.models.course_lesson_plan_model import (
    CourseLessonPlanModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
)

from apps.semesters.infrastructure.persistence.models.semester_model import (
    SemesterModel,
)


class MongoCourseLessonPlanRepository(
    CourseLessonPlanRepository
):

    def _to_entity(
        self,
        model: CourseLessonPlanModel,
    ):

        university = model.university
        subject = model.subject
        semester = model.semester

        if not university:
            return None

        if not subject:
            return None

        if not semester:
            return None

        academic_year = semester.academic_year

        if not academic_year:
            return None

        return CourseLessonPlan(
            course_lesson_plan_id=model.course_lesson_plan_id,

            university_id=university.university_id,
            university_name=university.name,

            subject_id=subject.subject_id,
            subject_name=subject.name,

            semester_id=semester.semester_id,
            semester_name=semester.name,
            semester_number=semester.semester_number,

            academic_year_id=academic_year.academic_year_id,
            academic_year_name=academic_year.name,

            total_lessons=model.total_lessons,
        )

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        models = CourseLessonPlanModel.objects(
            university=university,
        )

        return [
            self._to_entity(model)
            for model in models
        ]

    def get_by_subject_and_semester(
    self,
    university_id: str,
    subject_id: str,
    semester_id: str,
):
        semester = SemesterModel.objects(
            semester_id=semester_id,
        ).first()

        if semester is None:
            return None
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None: return None
        subject = SubjectModel.objects(
            subject_id=subject_id,
        ).first()
        if subject is None: return None
        model = CourseLessonPlanModel.objects(
            university=university,
            subject=subject,
            semester=semester,
        ).first()

        if model is None:
            return None

        return self._to_entity(model)
    def exists(
        self,
        university_id: str,
        subject_id: str,
        semester_id: str,
    ) -> bool:

        return (
            self.get_by_subject_and_semester(
                university_id=university_id,
                subject_id=subject_id,
                semester_id=semester_id,
            )
            is not None
        )

    def create(
    self,
    course_lesson_plan,
    university,
    subject,
    semester,
):
        # =====================================================
        # SUBJECT MODEL
        # =====================================================

        subject_model = SubjectModel.objects(
            subject_id=subject.subject_id,
            university=university,
        ).first()

        if not subject_model:
            raise ValueError(
                f"Không tìm thấy môn "
                f"'{subject.subject_id}'."
            )

        # =====================================================
        # SEMESTER MODEL
        # =====================================================

        semester_model = SemesterModel.objects(
            semester_id=semester.semester_id,
        ).first()

        if not semester_model:
            raise ValueError(
                f"Không tìm thấy học kỳ "
                f"'{semester.semester_id}'."
            )

        # =====================================================
        # CREATE MODEL
        # =====================================================

        model = CourseLessonPlanModel(
            course_lesson_plan_id=(
                course_lesson_plan.course_lesson_plan_id
            ),
            university=university,
            subject=subject_model,
            semester=semester_model,
            total_lessons=(
                course_lesson_plan.total_lessons
            ),
        )

        model.save()

        return course_lesson_plan