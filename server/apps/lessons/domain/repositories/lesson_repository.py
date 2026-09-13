from abc import ABC, abstractmethod

from apps.lessons.domain.entities.lesson_entity import Lesson


class LessonRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ) -> list[Lesson]:

        pass

    @abstractmethod
    def exists_by_number(
        self,
        university_id: str,
        lesson_number: int,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        lesson: Lesson,
    ) -> Lesson:
        pass

    @abstractmethod
    def get_max_lesson_number(
        self,
        university_id: str,
    ) -> int:
        pass

    def count_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_university_and_lesson_range(
        self,
        university_id: str,
        total_lessons: int,
    ):
        pass