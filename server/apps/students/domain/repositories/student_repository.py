from abc import ABC, abstractmethod


class StudentRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def exists_by_student_id(
        self,
        university_id: str,
        student_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_email(
        self,
        university_id: str,
        email: str,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        student,
        university,
        department,
    ):
        pass

    def find_by_student_id(
        self,
        university_id: str,
        student_id: str,
    ):
        pass
