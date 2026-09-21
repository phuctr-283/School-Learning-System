from apps.assignments.infrastructure.persistence.repositories.mongo_assignment_application_repository import MongoAssignmentApplicationRepository
from apps.assignments.application.use_cases.verify_student_assignment_qr import (
    VerifyStudentAssignmentQrUseCase,
)
from apps.assignments.infrastructure.services.assignment_application_id_generator import (
    AssignmentApplicationIdGenerator,
)

assignment_application_id_generator = AssignmentApplicationIdGenerator()

assignment_application_repository = (
    MongoAssignmentApplicationRepository(assignment_application_id_generator = AssignmentApplicationIdGenerator())
)

verify_student_assignment_qr_use_case = (
    VerifyStudentAssignmentQrUseCase(
        assignment_application_repository
    )
)