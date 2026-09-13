from abc import ABC, abstractmethod


class CourseLessonPlanRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass
    @abstractmethod
    def get_by_subject_and_semester(
        self,
        university_id: str,
        subject_id: str,
        semester_id: str,
    ):
        pass

    @abstractmethod
    def create(
        self,
        course_lesson_plan,
        university,
        subject,
        semester,
    ):
        pass

    @abstractmethod
    def exists(
        self,
        university_id: str,
        subject_id: str,
        semester_id: str,
    ) -> bool:
        pass