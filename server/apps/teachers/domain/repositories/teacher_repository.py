from abc import ABC, abstractmethod


class TeacherRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        teacher_id: str,
        university_id: str,
        department_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(
        self,
        teacher_id: str,
        department_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        teacher,
        department,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_department(
        self,
        department,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_name(
        self,
        name: str,
        department_id: str,
        university_id: str,
    ):
        raise NotImplementedError