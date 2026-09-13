from abc import ABC, abstractmethod


class DepartmentRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        department,
    ):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(
        self,
        department_id: str,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        department_id: str,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def exists_department_number(
        self,
        university_id: str,
        department_number: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_active_by_university(
        self,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_active_by_university_authenticated(
        self,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def find_by_number(
        self,
        university_id: str,
        department_number: str,
    ):
        raise NotImplementedError