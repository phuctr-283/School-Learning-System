from abc import ABC, abstractmethod


class ClassSectionLessonPlanRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
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
    def get_by_class_section_lesson_plan_id(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
    ):
        pass

    @abstractmethod
    def get_by_course_lesson_plan(
        self,
        university_id: str,
        course_lesson_plan_id: str,
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
        lessons,
    ):
        pass

    @abstractmethod
    def ensure_lesson_openings(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lessons,
    ):
        pass

    @abstractmethod
    def update_lesson_opening_status(
        self,
        university_id: str,
        class_section_lesson_plan_id: str,
        lesson_id: str,
        status: str,
        opened_at=None,
        closed_at=None,
    ):
        pass

    @abstractmethod
    def get_student_lessons(
        self,
        student_id: str,
        university_id: str,
        class_section_id: str,
    ):
        raise NotImplementedError