from abc import ABC, abstractmethod


class ClassSectionLessonPlanRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    def get_by_course_lesson_plan(
        self,
        university_id: str,
        course_lesson_plan_id: str,
    ):
        pass
    
    @abstractmethod
    def get_by_class_section(
        self,
        university_id: str,
        class_section_id: str,
    ):
        pass

    @abstractmethod
    def exists_by_class_section(
        self,
        university_id: str,
        class_section_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        entity,
        university_id: str,
        class_section_id: str,
        course_lesson_plan_id: str,
    ):
        pass
