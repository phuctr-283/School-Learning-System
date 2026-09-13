from abc import ABC, abstractmethod

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)


class AssignmentRepository(ABC):

    @abstractmethod
    def create(
        self,
        assignment: Assignment,
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