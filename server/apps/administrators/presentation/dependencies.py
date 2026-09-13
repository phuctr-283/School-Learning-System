from apps.users.application.use_cases.create_user import (
    CreateUserUseCase,
)

from apps.users.infrastructure.persistence.repositories.mongo_user_repository import (
    MongoUserRepository,
)

from apps.users.infrastructure.services.password_service import (
    PasswordService,
)

from apps.users.infrastructure.services.user_id_generator import (
    UserIdGenerator,
)

from apps.administrators.infrastructure.persistence.repositories.mongo_school_admin_repository import (
    MongoSchoolAdminRepository,
)

from apps.administrators.infrastructure.persistence.repositories.mongo_super_admin_repository import (
    MongoSuperAdminRepository,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.administrators.domain.services.school_admin_id_generator import (
    SchoolAdminIdGenerator,
)

from apps.administrators.domain.services.super_admin_id_generator import (
    SuperAdminIdGenerator,
)

from apps.administrators.application.use_cases.school_admin.register_school_admin import (
    RegisterSchoolAdminUseCase,
)

from apps.administrators.application.use_cases.super_admin.register_super_admin import (
    RegisterSuperAdminUseCase,
)

user_repository = MongoUserRepository()

password_service = PasswordService()

user_id_generator = UserIdGenerator()

create_user_use_case = CreateUserUseCase(
    user_repository=user_repository,
    password_service=password_service,
    user_id_generator=user_id_generator,
)


school_admin_repository = MongoSchoolAdminRepository()

super_admin_repository = MongoSuperAdminRepository()

university_repository = MongoUniversityRepository()


school_admin_id_generator = SchoolAdminIdGenerator()

super_admin_id_generator = SuperAdminIdGenerator()


register_school_admin_use_case = RegisterSchoolAdminUseCase(
    create_user_use_case=create_user_use_case,
    school_admin_repository=school_admin_repository,
    school_admin_id_generator=school_admin_id_generator,
    university_repository=university_repository,
)


register_super_admin_use_case = RegisterSuperAdminUseCase(
    create_user_use_case=create_user_use_case,
    super_admin_repository=super_admin_repository,
    super_admin_id_generator=super_admin_id_generator,
)
