from apps.assignments.infrastructure.persistence.repositories.mongo_assignment_repository import (
    MongoAssignmentRepository,
)

from apps.assignments.application.use_cases.create_assignment_use_case import (
    CreateAssignmentUseCase,
)

from apps.assignments.application.use_cases.get_assignments_use_case import (
    GetAssignmentsUseCase,
)

from apps.universities.infrastructure.persistence.repositories.mongo_university_repository import (
    MongoUniversityRepository,
)

from apps.departments.infrastructure.persistence.repositories.mongo_department_repository import (
    MongoDepartmentRepository,
)

from apps.subjects.infrastructure.persistence.repositories.mongo_subject_repository import (
    MongoSubjectRepository,
)

from apps.teachers.infrastructure.persistence.repositories.mongo_teacher_repository import (
    MongoTeacherRepository,
)


assignment_repository = MongoAssignmentRepository()
university_repository = MongoUniversityRepository()
department_repository = MongoDepartmentRepository()
subject_repository = MongoSubjectRepository()
teacher_repository = MongoTeacherRepository()


create_assignment_use_case = CreateAssignmentUseCase(
    assignment_repository=assignment_repository,
    university_repository=university_repository,
    department_repository=department_repository,
    subject_repository=subject_repository,
    teacher_repository=teacher_repository,
)


get_assignments_use_case = GetAssignmentsUseCase(
    assignment_repository=assignment_repository,
)