from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.teachers.infrastructure.persistence.repositories.mongo_teacher_repository import (
    MongoTeacherRepository,
)

from apps.departments.application.use_cases.get_university_departments import (
    GetUniversityDepartmentsUseCase,
)

from apps.departments.application.use_cases.get_active_departments import (
    GetActiveDepartmentsUseCase,
)

from apps.departments.application.use_cases.create_department import (
    CreateDepartmentUseCase,
)

department_repository = MongoDepartmentRepository()

university_repository = MongoUniversityRepository()

teacher_repository = MongoTeacherRepository()


get_university_departments_use_case = GetUniversityDepartmentsUseCase(
    department_repository
)

get_active_departments_use_case = GetActiveDepartmentsUseCase(
    department_repository=department_repository,
)

create_department_use_case = CreateDepartmentUseCase(
    department_repository,
    university_repository,
    teacher_repository,
)
