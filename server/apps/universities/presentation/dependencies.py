from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.universities.application.use_cases.create_university import (
    CreateUniversityUseCase,
)

from apps.universities.application.use_cases.get_universities import (
    GetUniversitiesUseCase,
)


university_repository = MongoUniversityRepository()

create_university_use_case = CreateUniversityUseCase(
    university_repository,
)

get_universities_use_case = GetUniversitiesUseCase(
    university_repository,
)