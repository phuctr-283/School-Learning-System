from apps.lessons.infrastructure.persistence.repositories.mongo_class_section_lesson_plan_repository import (
    MongoClassSectionLessonPlanRepository,
)

from apps.lessons.application.use_cases.get_lesson_openings_use_case import (
    GetLessonOpeningsUseCase,
)

from apps.lessons.application.use_cases.update_lesson_opening_status_use_case import (
    UpdateLessonOpeningStatusUseCase,
)


class_section_lesson_plan_repository = (
    MongoClassSectionLessonPlanRepository()
)


get_lesson_openings_use_case = (
    GetLessonOpeningsUseCase(
        class_section_lesson_plan_repository=(
            class_section_lesson_plan_repository
        ),
    )
)


update_lesson_opening_status_use_case = (
    UpdateLessonOpeningStatusUseCase(
        class_section_lesson_plan_repository=(
            class_section_lesson_plan_repository
        ),
    )
)