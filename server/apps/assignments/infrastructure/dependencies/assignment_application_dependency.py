from apps.assignments.infrastructure.persistence.repositories.mongo_assignment_application_repository import (
    MongoAssignmentApplicationRepository,
)
from apps.assignments.infrastructure.services.assignment_application_id_generator import (
    AssignmentApplicationIdGenerator,
)
from apps.assignments.application.use_cases.get_assignment_applications_use_case import (
    GetAssignmentApplicationsUseCase,
)
from apps.assignments.application.use_cases.update_assignment_application_class_section_status_use_case import (
    UpdateAssignmentApplicationClassSectionStatusUseCase,
)

from apps.assignments.application.use_cases.apply_assignment_use_case import (
    ApplyAssignmentUseCase,
)
assignment_application_id_generator = AssignmentApplicationIdGenerator()

assignment_application_repository = (
    MongoAssignmentApplicationRepository(assignment_application_id_generator = AssignmentApplicationIdGenerator())
)

apply_assignment_use_case = ApplyAssignmentUseCase(
    assignment_application_repository=(assignment_application_repository)
)

get_assignment_applications_use_case = (
    GetAssignmentApplicationsUseCase(
        assignment_application_repository=(
            assignment_application_repository
        ),
    )
)
update_assignment_application_class_section_status_use_case = (
    UpdateAssignmentApplicationClassSectionStatusUseCase(
        assignment_application_repository=(
            assignment_application_repository
        ),
    )
)