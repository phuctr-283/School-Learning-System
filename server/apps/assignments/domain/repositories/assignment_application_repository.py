from abc import ABC, abstractmethod


class AssignmentApplicationRepository(ABC):

    @abstractmethod
    def apply_to_class_sections(
        self,
        assignment_id: str,
        lesson_id: str,
        class_section_ids: list[str],
        teacher_email: str,
        max_attempts: int = 1,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        assignment_application_id: str,
        university_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_by_class_section_and_lesson(
        self,
        class_section_id: str,
        lesson_id: str,
        teacher_email: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def update_class_section_status(
        self,
        assignment_application_id: str,
        class_section_id: str,
        teacher_email: str,
        status: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def verify_student_assignment_qr(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
    ):
        raise NotImplementedError
