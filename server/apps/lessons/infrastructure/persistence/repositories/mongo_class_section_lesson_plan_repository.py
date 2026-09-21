from apps.lessons.domain.entities.class_section_lesson_plan_entity import (
    ClassSectionLessonPlan,
)

from apps.lessons.domain.entities.lesson_opening_entity import (
    LessonOpening,
)

from apps.lessons.domain.repositories.class_section_lesson_plan_repository import (
    ClassSectionLessonPlanRepository,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_opening_embedded import (
    ClassSectionLessonOpeningEmbedded,
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
from apps.lessons.application.dto.lesson_opening_dto import (
    LessonOpeningDTO,
)
from apps.class_sections.infrastructure.persistence.models.class_section_student_model import ClassSectionStudentModel
from apps.lessons.application.dto.student_class_section_lesson_dto import StudentClassSectionLessonDTO
class MongoClassSectionLessonPlanRepository(ClassSectionLessonPlanRepository):

    def _to_lesson_opening_entity(
        self,
        embedded,
    ):

        lesson = embedded.lesson

        if not lesson:
            return None

        return LessonOpening(
            lesson_id=lesson.lesson_id,
            lesson_number=lesson.lesson_number,
            lesson_name=lesson.name,
            status=embedded.status,
            opened_at=embedded.opened_at,
            closed_at=embedded.closed_at,
        )

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

        if not subject:
            return None

        semester = class_section.semester

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

        lesson_openings = []

        for embedded in model.lesson_openings or []:

            entity = self._to_lesson_opening_entity(embedded)

            if entity:
                lesson_openings.append(entity)

        lesson_openings.sort(key=lambda item: item.lesson_number)

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
            lesson_openings=(lesson_openings),
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

        models = list(
            ClassSectionLessonPlanModel.objects(
                university=university,
            )
        )

        return [
            entity for model in models if (entity := self._to_entity(model)) is not None
        ]

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

    def get_by_class_section_lesson_plan_id(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        model = ClassSectionLessonPlanModel.objects(
            university=university,
            class_section_lesson_plan_id=(class_section_lesson_plan_id),
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
            course_lesson_plan_id=(course_lesson_plan_id),
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
        university_id: str,
        class_section_id: str,
        course_lesson_plan_id: str,
        lessons,
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

        subject = class_section.subject

        if not subject:
            raise ValueError("Lớp học phần chưa có môn học.")

        if subject.university != university:
            raise ValueError("Lớp học phần không thuộc trường.")

        course_lesson_plan = CourseLessonPlanModel.objects(
            course_lesson_plan_id=(course_lesson_plan_id),
            university=university,
        ).first()

        if not course_lesson_plan:
            raise ValueError("Không tìm thấy kế hoạch môn học phần.")

        lesson_openings = [
            ClassSectionLessonOpeningEmbedded(
                lesson=lesson,
                status="locked",
                opened_at=None,
                closed_at=None,
            )
            for lesson in lessons
        ]

        model = ClassSectionLessonPlanModel(
            class_section_lesson_plan_id=(entity.class_section_lesson_plan_id),
            university=university,
            class_section=class_section,
            course_lesson_plan=(course_lesson_plan),
            is_custom=(entity.is_custom),
            custom_total_lessons=(entity.custom_total_lessons),
            lesson_openings=lesson_openings,
        )

        model.save()

        return self._to_entity(model)

    def ensure_lesson_openings(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lessons,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường.")

        model = ClassSectionLessonPlanModel.objects(
            university=university,
            class_section_lesson_plan_id=(class_section_lesson_plan_id),
        ).first()

        if not model:
            raise ValueError("Không tìm thấy kế hoạch lớp học phần.")

        existing_lesson_ids = {
            opening.lesson.lesson_id
            for opening in (model.lesson_openings or [])
            if opening.lesson
        }

        changed = False

        for lesson in lessons:

            if lesson.lesson_id in existing_lesson_ids:
                continue

            model.lesson_openings.append(
                ClassSectionLessonOpeningEmbedded(
                    lesson=lesson,
                    status="locked",
                    opened_at=None,
                    closed_at=None,
                )
            )

            existing_lesson_ids.add(lesson.lesson_id)

            changed = True

        if changed:
            model.save()

        return self._to_entity(model)

    def update_lesson_opening_status(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
        status: str,
        opened_at=None,
        closed_at=None,
    ):

        allowed_statuses = {
            "locked",
            "open",
            "closed",
        }

        if status not in allowed_statuses:
            raise ValueError("Trạng thái buổi học không hợp lệ.")

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường.")

        model = ClassSectionLessonPlanModel.objects(
            university=university,
            class_section_lesson_plan_id=(class_section_lesson_plan_id),
        ).first()

        if not model:
            raise ValueError("Không tìm thấy kế hoạch lớp học phần.")

        opening = None

        for item in model.lesson_openings or []:

            if item.lesson and item.lesson.lesson_id == lesson_id:
                opening = item
                break

        if not opening:
            raise ValueError("Không tìm thấy buổi học trong kế hoạch.")

        opening.status = status
        opening.opened_at = opened_at
        opening.closed_at = closed_at

        model.save()

        return self._to_entity(model)

    def get_student_lessons(
        self,
        student_id: str,
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
            university=university,
            status="active",
        ).first()

        if not class_section:
            raise ValueError("Không tìm thấy lớp học phần.")

        enrollment = ClassSectionStudentModel.objects(
            student__student_id=student_id,
            student__university=university,
            class_section=class_section,
        ).first()

        if not enrollment:
            raise ValueError("Sinh viên không thuộc lớp học phần này.")

        lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section=class_section,
                university=university,
            )
            .select_related()
            .first()
        )

        if not lesson_plan:
            return None

        course_lesson_plan = lesson_plan.course_lesson_plan

        subject = course_lesson_plan.subject
        semester = course_lesson_plan.semester
        academic_year = semester.academic_year

        lesson_openings = []

        for item in lesson_plan.lesson_openings or []:

            lesson = item.lesson

            if not lesson:
                continue

            lesson_openings.append(
                LessonOpeningDTO(
                    lesson_id=str(lesson.lesson_id),
                    lesson_number=lesson.lesson_number,
                    lesson_name=lesson.title,
                    status=item.status,
                    opened_at=item.opened_at,
                    closed_at=item.closed_at,
                )
            )

        return StudentClassSectionLessonDTO(
            class_section_id=str(class_section.class_section_id),
            academic_year_id=str(academic_year.academic_year_id),
            academic_year_name=academic_year.name,
            semester_id=str(semester.semester_id),
            semester_name=semester.name,
            semester_number=str(semester.semester_number),
            subject_id=str(subject.subject_id),
            subject_name=subject.name,
            group_number=class_section.group_number,
            lesson_openings=lesson_openings,
        )
