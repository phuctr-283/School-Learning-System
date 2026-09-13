from abc import ABC, abstractmethod


class SubjectLessonPlanRepository(ABC):

    @abstractmethod
    def create(
        self,
        subject_lesson_plan,
    ):
        pass

    @abstractmethod
    def exists_rule(
        self,
        university_id: str,
        semester_number: str,
        lesson_type: str,
        min_credits,
        max_credits,
    ) -> bool:
        pass

    @abstractmethod
    def get_subject_lesson_plans(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def get_by_semester_number(
        self,
        university_id: str,
        semester_number: str,
    ):
        pass

    def get_rule_for_subject(
        self,
        university_id: str,
        subject,
        semester_number: str,
    ):
        pass

    def get_rules_by_semester_number(
        self,
        university_id: str,
        semester_number: str,
    ):
        pass
