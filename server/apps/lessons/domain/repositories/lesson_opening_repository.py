from abc import ABC, abstractmethod


class LessonOpeningRepository(ABC):

    @abstractmethod
    def exists_by_class_section_plan_and_lesson(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
    ):
        pass


    @abstractmethod
    def create(
        self,
        entity,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
    ):
        pass


    @abstractmethod
    def get_by_class_section_lesson_plan(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):
        pass