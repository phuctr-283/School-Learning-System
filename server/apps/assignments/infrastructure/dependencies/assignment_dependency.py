from apps.assignments.infrastructure.persistence.repositories.mongo_assignment_repository import (
    MongoAssignmentRepository,
)

from apps.assignments.application.use_cases.create_assignment_use_case import (
    CreateAssignmentUseCase,
)

from apps.assignments.application.use_cases.get_assignments_use_case import (
    GetAssignmentsUseCase,
)

from apps.assignments.application.use_cases.get_assignments_by_subject_use_case import (
    GetAssignmentsBySubjectUseCase,
)

from apps.assignments.application.use_cases.get_assignment_content_use_case import (
    GetAssignmentContentUseCase,
)

from apps.subjects.infrastructure.persistence.repositories.mongo_subject_repository import (
    MongoSubjectRepository,
)

from apps.assignments.infrastructure.services.assignment_id_generator import (
    AssignmentIdGenerator,
)

assignment_repository = MongoAssignmentRepository()

subject_repository = MongoSubjectRepository()

assignment_id_generator = AssignmentIdGenerator()


create_assignment_use_case = CreateAssignmentUseCase(
    assignment_repository=assignment_repository,
    assignment_id_generator=assignment_id_generator,
    subject_repository=subject_repository,
)


get_assignments_use_case = GetAssignmentsUseCase(
    assignment_repository=assignment_repository,
)


get_assignments_by_subject_use_case = GetAssignmentsBySubjectUseCase(
    assignment_repository=assignment_repository,
)


get_assignment_content_use_case = GetAssignmentContentUseCase(
    assignment_repository=assignment_repository,
)



