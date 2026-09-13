from apps.lessons.application.use_cases.get_semester_lesson_plans import (
    GetSemesterLessonPlansUseCase,
)
from apps.lessons.application.use_cases.create_semester_lesson_plan import (
    CreateSemesterLessonPlanUseCase,
)
from apps.lessons.infrastructure.persistence.repositories.mongo_semester_lesson_plan_repository import (
    MongoSemesterLessonPlanRepository,
)
from apps.lessons.infrastructure.persistence.repositories.mongo_subject_lesson_plan_repository import (
    MongoSubjectLessonPlanRepository,
)


from apps.semesters.infrastructure.persistence.repositories.mongo_semester_repository import (
    MongoSemesterRepository,
)


from apps.academic_years.infrastructure.persistence.repositories.mongo_academic_year_repository import (
    MongoAcademicYearRepository,
)


from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)
from apps.lessons.infrastructure.persistence.repositories.mongo_lesson_repository import (
    MongoLessonRepository,
)
from apps.lessons.infrastructure.services.semester_lesson_plan_id_generator import (
    SemesterLessonPlanIdGenerator,
)

university_repository = MongoUniversityRepository()

academic_year_repository = MongoAcademicYearRepository()

lesson_repository = MongoLessonRepository()

semester_repository = MongoSemesterRepository()

semester_lesson_plan_repository = MongoSemesterLessonPlanRepository()

subject_lesson_plan_repository = MongoSubjectLessonPlanRepository()

semester_lesson_plan_id_generator = SemesterLessonPlanIdGenerator()

get_semester_lesson_plans_use_case = GetSemesterLessonPlansUseCase(
    semester_lesson_plan_repository,
)
create_semester_lesson_plan_use_case = CreateSemesterLessonPlanUseCase(
    university_repository=university_repository,
    academic_year_repository=academic_year_repository,
    semester_repository=semester_repository,
    semester_lesson_plan_repository=semester_lesson_plan_repository,
    subject_lesson_plan_repository=subject_lesson_plan_repository,
    semester_lesson_plan_id_generator=semester_lesson_plan_id_generator,
    lesson_repository=lesson_repository,
)
