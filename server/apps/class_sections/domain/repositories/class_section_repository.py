from abc import ABC, abstractmethod


class ClassSectionRepository(ABC):

    @abstractmethod
    def get_by_university(
        self,
        university_id: str,
    ):
        pass

    @abstractmethod
    def exists_by_group(
        self,
        university_id: str,
        subject_id: str,
        group_number: int,
        semester_id: str,
        academic_year_id: str,
    ) -> bool:
        pass

    @abstractmethod
    def create(
        self,
        class_section,
        subject,
        teacher,
        semester,
        academic_year,
    ):
        pass

    @abstractmethod
    def update_status(
        self,
        university_id: str,
        class_section_id: str,
        status: str,
    ):
        pass

    @abstractmethod
    def get_teacher_subjects(
        university_id,
        department_id,
        teacher_id,
    ):
        pass

    @abstractmethod
    def get_teacher_class_sections(
        self,
        university_id: str,
        department_id: str,
        teacher_id: str,
        subject_id: str,
    ):
        pass

    def find_by_import_info_and_teacher(
    self,
    university_id: str,
    subject_name: str,
    group_number: int,
    semester_number: int,
    academic_year_name: str,
    teacher_id: str,
): pass