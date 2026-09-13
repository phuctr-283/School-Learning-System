from abc import ABC, abstractmethod


class SemesterRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_active_planned(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        university_id: str,
        semester_id: str,
    ):
        pass

    @abstractmethod
    def get_by_name(
        self,
        university_id: str,
        academic_year_id: str,
        name: str,
    ):
        pass

    def get_by_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
    ):
        pass

    @abstractmethod
    def get_by_academic_year_and_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
    ):
        pass

    @abstractmethod
    def exists_by_number(
        self,
        university_id: str,
        academic_year_id: str,
        semester_number: str,
    ):
        pass

    @abstractmethod
    def update_status(
        self,
        university_id: str,
        semester_id: str,
        status: str,
    ):
        pass

    @abstractmethod
    def create(
        self,
        semester,
        academic_year,
    ):
        pass
