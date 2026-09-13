from apps.lessons.application.use_cases.create_subject_lesson_plan import (
    CreateSubjectLessonPlanUseCase,
)

from apps.lessons.application.use_cases.get_subject_lesson_plans import (
    GetSubjectLessonPlansUseCase,
)

from apps.lessons.infrastructure.services.subject_lesson_plan_id_generator import (
    SubjectLessonPlanIdGenerator,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_subject_lesson_plan_repository import (
    MongoSubjectLessonPlanRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_lesson_repository import (
    MongoLessonRepository,
)

lesson_repository = MongoLessonRepository()
subject_lesson_plan_repository = (
    MongoSubjectLessonPlanRepository()
)

university_repository = (
    MongoUniversityRepository()
)

subject_lesson_plan_id_generator = (
    SubjectLessonPlanIdGenerator()
)
create_subject_lesson_plan_use_case = (
    CreateSubjectLessonPlanUseCase(
        repository=subject_lesson_plan_repository,
        university_repository=university_repository,
        lesson_repository=lesson_repository,
        id_generator=subject_lesson_plan_id_generator,
    )
)


get_subject_lesson_plans_use_case = (
    GetSubjectLessonPlansUseCase(
        subject_lesson_plan_repository
    )
)