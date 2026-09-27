from apps.assignments.infrastructure.persistence.repositories.mongo_student_assignment_repository import (
    MongoStudentAssignmentRepository,
)

from apps.assignments.application.use_cases.get_student_assignment_use_case import (
    GetStudentAssignmentUseCase,
)

from apps.assignments.application.use_cases.save_student_assignment_use_case import (
    SaveStudentAssignmentUseCase,
)

from apps.assignments.application.use_cases.submit_student_assignment_use_case import (
    SubmitStudentAssignmentUseCase,
)
from apps.assignments.application.use_cases.get_student_assignment_history_use_case import GetStudentAssignmentHistoryUseCase

def get_student_assignment_repository():

    return MongoStudentAssignmentRepository()


def get_student_assignment_use_case():

    repository = get_student_assignment_repository()
    return GetStudentAssignmentUseCase(repository)


def get_save_student_assignment_use_case():

    repository = get_student_assignment_repository()
    return SaveStudentAssignmentUseCase(repository)


def get_submit_student_assignment_use_case():

    repository = get_student_assignment_repository()
    return SubmitStudentAssignmentUseCase(repository)

def get_student_assignment_history_use_case():
    repository = MongoStudentAssignmentRepository()

    return GetStudentAssignmentHistoryUseCase(
        student_assignment_repository=repository,
    )