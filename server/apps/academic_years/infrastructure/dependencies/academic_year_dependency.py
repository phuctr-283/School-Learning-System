from apps.academic_years.application.use_cases.get_academic_years import (
    GetAcademicYearsUseCase,
)

from apps.academic_years.application.use_cases.create_academic_year import (
    CreateAcademicYearUseCase,
)
from apps.academic_years.application.use_cases.get_active_and_planned_academic_years import (
    GetActiveAndPlannedAcademicYearsUseCase,
)
from apps.academic_years.application.use_cases.update_academic_year_statuses import (
    UpdateAcademicYearStatusesUseCase,
)

from apps.academic_years.infrastructure.persistence.repositories.mongo_academic_year_repository import (
    MongoAcademicYearRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)


academic_year_repository = (
    MongoAcademicYearRepository()
)

university_repository = (
    MongoUniversityRepository()
)


update_academic_year_statuses_use_case = (
    UpdateAcademicYearStatusesUseCase(
        academic_year_repository,
    )
)

get_academic_years_use_case = (
    GetAcademicYearsUseCase(
        academic_year_repository,
        update_academic_year_statuses_use_case,
    )
)
get_active_and_planned_academic_years_use_case = (
    GetActiveAndPlannedAcademicYearsUseCase(
        academic_year_repository
    )
)
create_academic_year_use_case = (
    CreateAcademicYearUseCase(
        academic_year_repository,
        university_repository,
        update_academic_year_statuses_use_case,
    )
)