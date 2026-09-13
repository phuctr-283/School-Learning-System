from apps.lessons.infrastructure.persistence.repositories.mongo_course_lesson_plan_repository import (
    MongoCourseLessonPlanRepository,
)

from apps.lessons.application.use_cases.get_course_lesson_plans import (
    GetCourseLessonPlansUseCase,
)

from apps.lessons.application.use_cases.ensure_course_lesson_plans import (
    EnsureCourseLessonPlansUseCase,
)

from apps.class_sections.infrastructure.persistence.repositories.mongo_class_section_repository import (
    MongoClassSectionRepository,
)

from apps.lessons.infrastructure.persistence.repositories.mongo_subject_lesson_plan_repository import (
    MongoSubjectLessonPlanRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.subjects.infrastructure.persistence.repositories.mongo_subject_repository import (
    MongoSubjectRepository,
)

from apps.semesters.infrastructure.persistence.repositories.mongo_semester_repository import (
    MongoSemesterRepository,
)

from apps.lessons.infrastructure.services.course_lesson_plan_id_generator import (
    CourseLessonPlanIdGenerator,
)

# =========================================================
# REPOSITORIES
# =========================================================

course_lesson_plan_repository = MongoCourseLessonPlanRepository()

class_section_repository = MongoClassSectionRepository()

subject_lesson_plan_repository = MongoSubjectLessonPlanRepository()

university_repository = MongoUniversityRepository()

subject_repository = MongoSubjectRepository()

semester_repository = MongoSemesterRepository()


# =========================================================
# ID GENERATOR
# =========================================================

course_lesson_plan_id_generator = CourseLessonPlanIdGenerator()


# =========================================================
# GET
# =========================================================

get_course_lesson_plans_use_case = GetCourseLessonPlansUseCase(
    course_lesson_plan_repository=(course_lesson_plan_repository),
)


# =========================================================
# ENSURE
# =========================================================

ensure_course_lesson_plans_use_case = EnsureCourseLessonPlansUseCase(
    class_section_repository=(class_section_repository),
    course_lesson_plan_repository=(course_lesson_plan_repository),
    subject_lesson_plan_repository=(subject_lesson_plan_repository),
    university_repository=(university_repository),
    subject_repository=(subject_repository),
    semester_repository=(semester_repository),
    course_lesson_plan_id_generator=(course_lesson_plan_id_generator),
)
