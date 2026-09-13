from abc import ABC, abstractmethod


class SemesterLessonPlanRepository(ABC):
    @abstractmethod
    def get_by_university(self, university_id: str):
        pass

    @abstractmethod
    def get_all(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_id(
        self,
        university_id: str,
        semester_lesson_plan_id: str,
    ):
        pass

    @abstractmethod
    def get_by_semester(
        self,
        university_id: str,
        semester_id: str,
    ):
        pass

    @abstractmethod
    def exists_by_semester(
        self,
        university_id: str,
        semester_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        entity,
        university,
        semester,
    ):
        pass
