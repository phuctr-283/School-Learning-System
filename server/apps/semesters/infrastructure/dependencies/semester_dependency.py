from apps.semesters.infrastructure.persistence.repositories.mongo_semester_repository import (
    MongoSemesterRepository,
)
from apps.academic_years.infrastructure.persistence.repositories.mongo_academic_year_repository import (
    MongoAcademicYearRepository,
)

from apps.semesters.application.use_cases.create_semester import (
    CreateSemesterUseCase,
)

from apps.semesters.application.use_cases.get_semesters import (
    GetSemestersUseCase,
)
from apps.semesters.application.use_cases.get_active_planned_semesters import (
    GetActivePlannedSemestersUseCase,
)
from apps.semesters.application.use_cases.update_semester_statuses import (
    UpdateSemesterStatusesUseCase,
)

semester_repository = MongoSemesterRepository()

academic_year_repository = MongoAcademicYearRepository()

update_semester_statuses_use_case = UpdateSemesterStatusesUseCase(
    semester_repository,
)

get_semesters_use_case = GetSemestersUseCase(
    semester_repository,
    update_semester_statuses_use_case,
)
get_active_planned_semesters_dependency = GetActivePlannedSemestersUseCase(
    semester_repository
)
create_semester_use_case = CreateSemesterUseCase(
    semester_repository,
    academic_year_repository,
    update_semester_statuses_use_case,
)
