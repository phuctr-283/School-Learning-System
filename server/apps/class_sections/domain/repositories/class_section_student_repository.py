from abc import ABC, abstractmethod


class ClassSectionStudentRepository(
    ABC
):

    @abstractmethod
    def exists(
        self,
        class_section,
        student,
    ):
        raise NotImplementedError

    @abstractmethod
    def add(
        self,
        class_section,
        student,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_students_by_class_section(
        self,
        class_section,
    ):
        raise NotImplementedError