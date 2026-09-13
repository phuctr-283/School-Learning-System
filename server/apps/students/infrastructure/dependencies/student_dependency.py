from apps.students.infrastructure.persistence.repositories.mongo_student_repository import (
    MongoStudentRepository,
)

from apps.students.application.use_cases.get_students import (
    GetStudentsUseCase,
)

from apps.students.application.use_cases.import_students import (
    ImportStudentsUseCase,
)

from apps.students.application.use_cases.create_student_account import (
    CreateStudentAccountUseCase,
)

from apps.students.infrastructure.services.excel_student_import_service import (
    ExcelStudentImportService,
)

from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.dependencies.create_user_dependency import (
    create_user_use_case,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

student_repository = MongoStudentRepository()

department_repository = MongoDepartmentRepository()

user_repository = MongoUserRepository()

university_repository = MongoUniversityRepository()


excel_student_import_service = ExcelStudentImportService()


create_student_account_use_case = CreateStudentAccountUseCase(
    create_user_use_case=(create_user_use_case()),
)


get_students_use_case = GetStudentsUseCase(
    student_repository=(student_repository),
)

import_students_use_case = ImportStudentsUseCase(
    student_repository=(student_repository),
    university_repository=(university_repository),
    department_repository=(department_repository),
    user_repository=(user_repository),
    create_user_use_case=(create_user_use_case()),
)
