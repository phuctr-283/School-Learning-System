from abc import ABC, abstractmethod


class SubjectRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def exists_by_id(
        self,
        subject_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        subject,
        university,
        department,
    ):
        pass

    @abstractmethod
    def get_by_name(
        self,
        name: str,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        university_id: str,
        subject_id: str,
    ):
        pass