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
        self,
        university_id: str,
        username: str,
    ):
        pass

    @abstractmethod
    def get_teacher_active_subjects(
        self,
        university_id: str,
        username: str,
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
        university_id,
        subject_name,
        group_number,
        semester_number,
        academic_year_name,
        teacher_id,
    ):
        pass
    @abstractmethod
    def get_teacher_active_planned_subjects(
        self,
        university_id: str,
        username: str,
        academic_year_id: str,
        semester_id: str,
    ):
        raise NotImplementedError
    @abstractmethod
    def get_teacher_active_planned_class_sections(
        self,
        university_id: str,
        username: str,
        subject_id: str,
        academic_year_id: str,
        semester_id: str,
    ):
        raise NotImplementedError