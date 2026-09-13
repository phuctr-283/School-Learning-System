from apps.lessons.domain.entities.class_section_lesson_plan_entity import (
    ClassSectionLessonPlan,
)

from apps.lessons.domain.repositories.class_section_lesson_plan_repository import (
    ClassSectionLessonPlanRepository,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)
from apps.lessons.infrastructure.persistence.models.course_lesson_plan_model import (
    CourseLessonPlanModel,
)


class MongoClassSectionLessonPlanRepository(ClassSectionLessonPlanRepository):

    def _to_entity(
        self,
        model: ClassSectionLessonPlanModel,
    ):

        university = model.university
        class_section = model.class_section
        course_lesson_plan = model.course_lesson_plan

        if not university:
            return None

        if not class_section:
            return None

        if not course_lesson_plan:
            return None

        subject = class_section.subject
        semester = class_section.semester

        if not subject:
            return None

        if not semester:
            return None

        academic_year = semester.academic_year

        if not academic_year:
            return None

        course_total_lessons = course_lesson_plan.total_lessons

        if model.is_custom:

            effective_total_lessons = model.custom_total_lessons

        else:

            effective_total_lessons = course_total_lessons

        return ClassSectionLessonPlan(
            class_section_lesson_plan_id=(model.class_section_lesson_plan_id),
            university_id=(university.university_id),
            university_name=(university.name),
            course_lesson_plan_id=(course_lesson_plan.course_lesson_plan_id),
            class_section_id=(class_section.class_section_id),
            group_number=(class_section.group_number),
            subject_id=(subject.subject_id),
            subject_name=(subject.name),
            semester_id=(semester.semester_id),
            semester_name=(semester.name),
            semester_number=(semester.semester_number),
            academic_year_id=(academic_year.academic_year_id),
            academic_year_name=(academic_year.name),
            total_lessons=(course_total_lessons),
            is_custom=(model.is_custom),
            custom_total_lessons=(model.custom_total_lessons),
            effective_total_lessons=(effective_total_lessons),
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

        models = ClassSectionLessonPlanModel.objects(
            university=university,
        )

        return [self._to_entity(model) for model in models]

    def get_by_class_section(
        self,
        university_id: str,
        class_section_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
        ).first()

        if not class_section:
            return None
        subject = class_section.subject

        if not subject:
            return None

        if subject.university != university:
            return None

        model = ClassSectionLessonPlanModel.objects(
            university=university,
            class_section=class_section,
        ).first()
        if not model:
            return None
        return self._to_entity(model)

    def get_by_course_lesson_plan(
        self,
        university_id: str,
        course_lesson_plan_id: str,
    ):
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        course_lesson_plan = CourseLessonPlanModel.objects(
            course_lesson_plan_id=course_lesson_plan_id,
            university=university,
        ).first()

        if not course_lesson_plan:
            return []

        models = ClassSectionLessonPlanModel.objects(
            university=university,
            course_lesson_plan=course_lesson_plan,
        )

        return [
            entity for model in models if (entity := self._to_entity(model)) is not None
        ]

    def exists_by_class_section(
        self,
        university_id: str,
        class_section_id: str,
    ) -> bool:

        return (
            self.get_by_class_section(
                university_id=university_id,
                class_section_id=class_section_id,
            )
            is not None
        )

    def create(
        self,
        entity,
        university_id,
        class_section_id,
        course_lesson_plan_id,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường.")

        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
        ).first()

        if not class_section:
            raise ValueError("Không tìm thấy lớp học phần.")

        course_lesson_plan = CourseLessonPlanModel.objects(
            course_lesson_plan_id=course_lesson_plan_id,
            university=university,
        ).first()

        if not course_lesson_plan:
            raise ValueError("Không tìm thấy kế hoạch môn học phần.")

        model = ClassSectionLessonPlanModel(
            class_section_lesson_plan_id=(entity.class_section_lesson_plan_id),
            university=university,
            class_section=class_section,
            course_lesson_plan=course_lesson_plan,
            is_custom=entity.is_custom,
            custom_total_lessons=(entity.custom_total_lessons),
        )

        model.save()

        return self._to_entity(model)

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
            ClassSectionLessonPlanModel.objects(
                university=university,
            )
        )

        return [self._to_entity(model) for model in models]
