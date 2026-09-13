from apps.lessons.application.use_cases.ensure_lesson_openings_use_case import (
    EnsureLessonOpeningsUseCase,
)

from apps.lessons.application.use_cases.get_lesson_openings_use_case import (
    GetLessonOpeningsUseCase,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_lesson_opening_repository import (
    MongoLessonOpeningRepository,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_lesson_repository import (
    MongoLessonRepository,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_class_section_lesson_plan_repository import (
    MongoClassSectionLessonPlanRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.lessons.infrastructure.services.lesson_opening_id_generator import (
    LessonOpeningIdGenerator,
)


lesson_opening_repository = (
    MongoLessonOpeningRepository()
)

lesson_repository = (
    MongoLessonRepository()
)

class_section_lesson_plan_repository = (
    MongoClassSectionLessonPlanRepository()
)

university_repository = (
    MongoUniversityRepository()
)

lesson_opening_id_generator = (
    LessonOpeningIdGenerator()
)


ensure_lesson_openings_use_case = (
    EnsureLessonOpeningsUseCase(

        class_section_lesson_plan_repository=(
            class_section_lesson_plan_repository
        ),

        lesson_opening_repository=(
            lesson_opening_repository
        ),

        lesson_repository=(
            lesson_repository
        ),

        university_repository=(
            university_repository
        ),

        lesson_opening_id_generator=(
            lesson_opening_id_generator
        ),
    )
)


get_lesson_openings_use_case = (
    GetLessonOpeningsUseCase(

        lesson_opening_repository=(
            lesson_opening_repository
        ),
    )
)