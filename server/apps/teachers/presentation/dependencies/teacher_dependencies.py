from apps.teachers.application.use_cases.get_university_teachers import (
    GetUniversityTeachersUseCase,
)

from apps.teachers.infrastructure.persistence.repositories.mongo_teacher_repository import (
    MongoTeacherRepository,
)
from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

from apps.teachers.application.use_cases.register_teacher import (
    RegisterTeacherUseCase,
)

teacher_repository = MongoTeacherRepository()

university_repository = MongoUniversityRepository()

department_repository = MongoDepartmentRepository()
get_teachers_use_case = GetUniversityTeachersUseCase(teacher_repository)
register_teacher_use_case = RegisterTeacherUseCase(
    teacher_repository,
    university_repository,
    department_repository,
)
