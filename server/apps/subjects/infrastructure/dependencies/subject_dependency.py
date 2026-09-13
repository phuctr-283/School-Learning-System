from apps.subjects.application.use_cases.get_subjects_use_case import (
    GetSubjectsUseCase,
)
from apps.subjects.application.use_cases.create_subject import (
    CreateSubjectUseCase,
)
from apps.subjects.infrastructure.persistence.repositories.mongo_subject_repository import (
    MongoSubjectRepository,
)
from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

subject_repository = MongoSubjectRepository()
university_repository = MongoUniversityRepository()

department_repository = MongoDepartmentRepository()

get_subjects_use_case = GetSubjectsUseCase(
    subject_repository=subject_repository,
)
create_subject_use_case = CreateSubjectUseCase(
    subject_repository=subject_repository,
    university_repository=university_repository,
    department_repository=department_repository,
)
