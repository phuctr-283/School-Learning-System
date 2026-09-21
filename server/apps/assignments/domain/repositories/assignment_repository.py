from abc import ABC, abstractmethod

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assignments.application.dto.assignment_list_dto import (
    AssignmentListDTO,
)
from apps.assignments.application.dto.assignment_content_dto import AssignmentContentDTO

class AssignmentRepository(ABC):

    @abstractmethod
    def create_by_teacher_email(
        self,
        assignment: Assignment,
        teacher_email: str,
    ) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        assignment_id: str,
        university_id: str,
    ) -> Assignment | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_teacher(
        self,
        teacher_id: str,
        university_id: str,
        department_id: str | None = None,
    ) -> list[Assignment]:
        raise NotImplementedError

    @abstractmethod
    def get_assignments(
        self,
        university_id: str,
        teacher_email: str,
    ) -> list[AssignmentListDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_assignments_by_subject(
        self,
        university_id: str,
        teacher_email: str,
        subject_id: str,
    ) -> list[AssignmentListDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_content_by_id(
        self,
        assignment_id: str,
        university_id: str,
    ) -> AssignmentContentDTO | None:
        raise NotImplementedError
