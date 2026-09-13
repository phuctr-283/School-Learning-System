from apps.lessons.application.use_cases.get_lessons import (
    GetLessonsUseCase,
)
from apps.lessons.application.use_cases.create_lesson import (
    CreateLessonUseCase,
)
from apps.lessons.infrastructure.persistence.repositories.mongo_lesson_repository import (
    MongoLessonRepository,
)
from apps.lessons.application.use_cases.ensure_lesson_plans_use_case import (
    EnsureLessonPlansUseCase,
)

from apps.lessons.infrastructure.dependencies.course_lesson_plan_dependency import (
    ensure_course_lesson_plans_use_case
)

from apps.lessons.infrastructure.dependencies.class_section_lesson_plan_dependency import (
    ensure_class_section_lesson_plans_use_case
)
from apps.lessons.infrastructure.dependencies.lesson_opening_dependency import ensure_lesson_openings_use_case
lesson_repository = MongoLessonRepository()

get_lessons_use_case = GetLessonsUseCase(
    lesson_repository,
)
create_lesson_use_case = CreateLessonUseCase(
    lesson_repository=lesson_repository,
)
ensure_lesson_plans_dependency = (
    EnsureLessonPlansUseCase(
        ensure_course_lesson_plans_use_case=(
            ensure_course_lesson_plans_use_case
        ),
        ensure_class_section_lesson_plans_use_case=(
            ensure_class_section_lesson_plans_use_case
        ),
        ensure_lesson_openings_use_case= ensure_lesson_openings_use_case,
    )
)