from datetime import datetime
from apps.lessons.domain.entities.lesson_opening_entity import (
    LessonOpening,
)
from apps.lessons.domain.repositories.lesson_opening_repository import (
    LessonOpeningRepository,
)

from apps.lessons.infrastructure.persistence.models.lesson_opening_model import (
    LessonOpeningModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.lessons.infrastructure.persistence.models.lesson_model import (
    LessonModel,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)


class MongoLessonOpeningRepository(
    LessonOpeningRepository
):


    def exists_by_class_section_plan_and_lesson(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
    ):

        university = (
            UniversityModel.objects(
                university_id=university_id,
            ).first()
        )

        if not university:
            return False


        class_section_lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section_lesson_plan_id=(
                    class_section_lesson_plan_id
                ),
                university=university,
            ).first()
        )

        if not class_section_lesson_plan:
            return False


        lesson = (
            LessonModel.objects(
                lesson_id=lesson_id,
                university=university,
            ).first()
        )

        if not lesson:
            return False


        return LessonOpeningModel.objects(
            university=university,
            class_section_lesson_plan=(
                class_section_lesson_plan
            ),
            lesson=lesson,
        ).first() is not None


    def create(
        self,
        entity,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
    ):

        university = (
            UniversityModel.objects(
                university_id=university_id,
            ).first()
        )

        if not university:
            raise ValueError(
                "Không tìm thấy trường."
            )


        class_section_lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section_lesson_plan_id=(
                    class_section_lesson_plan_id
                ),
                university=university,
            ).first()
        )

        if not class_section_lesson_plan:
            raise ValueError(
                "Không tìm thấy kế hoạch lớp học phần."
            )


        lesson = (
            LessonModel.objects(
                lesson_id=lesson_id,
                university=university,
            ).first()
        )

        if not lesson:
            raise ValueError(
                "Không tìm thấy buổi học."
            )


        model = LessonOpeningModel(
            lesson_opening_id=(
                entity.lesson_opening_id
            ),

            university=university,

            class_section_lesson_plan=(
                class_section_lesson_plan
            ),

            lesson=lesson,

            status=entity.status,

            opened_at=entity.opened_at,

            closed_at=entity.closed_at,

            created_at=(
                entity.created_at
                or datetime.now()
            ),

            updated_at=(
                entity.updated_at
                or datetime.now()
            ),
        )

        model.save()

        return self._to_entity(model)


    def get_by_class_section_lesson_plan(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):

        university = (
            UniversityModel.objects(
                university_id=university_id,
            ).first()
        )

        if not university:
            return []


        class_section_lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section_lesson_plan_id=(
                    class_section_lesson_plan_id
                ),
                university=university,
            ).first()
        )

        if not class_section_lesson_plan:
            return []


        models = list(
            LessonOpeningModel.objects(
                university=university,
                class_section_lesson_plan=(
                    class_section_lesson_plan
                ),
            )
            .select_related()
        )


        models.sort(
            key=lambda item: item.lesson.lesson_number
        )


        return [
            self._to_entity(model)
            for model in models
        ]


    def _to_entity(
        self,
        model,
    ):

        return LessonOpening(
            lesson_opening_id=(
                model.lesson_opening_id
            ),

            university_id=(
                model.university.university_id
            ),

            university_name=(
                model.university.name
            ),

            class_section_lesson_plan_id=(
                model
                .class_section_lesson_plan
                .class_section_lesson_plan_id
            ),

            lesson_id=(
                model.lesson.lesson_id
            ),

            lesson_number=(
                model.lesson.lesson_number
            ),

            lesson_name=(
                model.lesson.name
            ),

            status=model.status,

            opened_at=model.opened_at,

            closed_at=model.closed_at,

            created_at=model.created_at,

            updated_at=model.updated_at,
        )