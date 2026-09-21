from abc import ABC, abstractmethod


class StudentAssignmentRepository(ABC):

    @abstractmethod
    def get_student_assignment(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def save_answers(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
        attempt_id: str,
        answers: dict,
    ):
        raise NotImplementedError

    @abstractmethod
    def submit_assignment(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
        attempt_id: str,
        answers: dict,
    ):
        raise NotImplementedError