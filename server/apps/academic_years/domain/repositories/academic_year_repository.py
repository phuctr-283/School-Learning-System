from abc import ABC, abstractmethod


class AcademicYearRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        university_id: str,
        academic_year_id: str,
    ):
        pass
    @abstractmethod
    def create(
        self,
        academic_year,
        university,
    ):
        pass

    @abstractmethod
    def exists_by_name(
        self,
        university,
        name: str,
    ) -> bool:
        pass

    @abstractmethod
    def find_by_id(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def update_status(
        self,
        university_id: str,
        academic_year_id: str,
        status: str,
    ):
        pass

    def get_active_and_planned_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_academic_year_by_id(
        self,
        university_id: str,
        academic_year_id: str,
    ):
        pass

    @abstractmethod
    def get_by_name(
        self,
        university_id: str,
        name: str,
    ):
        pass
