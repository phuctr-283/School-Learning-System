from apps.lessons.infrastructure.persistence.repositories.mongo_course_lesson_plan_repository import (
    MongoCourseLessonPlanRepository,
)

from apps.lessons.application.use_cases.get_class_section_lesson_plans import (
    GetClassSectionLessonPlansUseCase,
)

from apps.lessons.application.use_cases.ensure_class_section_lesson_plans import (
    EnsureClassSectionLessonPlansUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_class_section_lesson_plan_repository import (
    MongoClassSectionLessonPlanRepository,
)

from apps.lessons.infrastructure.services.class_section_lesson_plan_id_generator import (
    ClassSectionLessonPlanIdGenerator,
)

# =========================================================
# REPOSITORIES
# =========================================================

class_section_lesson_plan_repository = MongoClassSectionLessonPlanRepository()

course_lesson_plan_repository = MongoCourseLessonPlanRepository()

class_section_repository = MongoClassSectionRepository()

university_repository = MongoUniversityRepository()


# =========================================================
# ID GENERATOR
# =========================================================

class_section_lesson_plan_id_generator = ClassSectionLessonPlanIdGenerator()


# =========================================================
# GET
# =========================================================

get_class_section_lesson_plans_use_case = GetClassSectionLessonPlansUseCase(
    class_section_lesson_plan_repository=(class_section_lesson_plan_repository),
)


# =========================================================
# ENSURE
# =========================================================

ensure_class_section_lesson_plans_use_case = EnsureClassSectionLessonPlansUseCase(
    class_section_repository=(class_section_repository),
    class_section_lesson_plan_repository=(class_section_lesson_plan_repository),
    course_lesson_plan_repository=(course_lesson_plan_repository),
    university_repository=(university_repository),
    class_section_lesson_plan_id_generator=(class_section_lesson_plan_id_generator),
)
