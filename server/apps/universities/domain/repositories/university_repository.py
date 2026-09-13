from abc import ABC, abstractmethod


class UniversityRepository(ABC):

    @abstractmethod
    def create(self, university):
        pass

    @abstractmethod
    def find_by_id(self, university_id):
        pass

    @abstractmethod
    def find_by_name(self, name):
        pass

    @abstractmethod
    def find_by_domain(self, domain):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_active(self):
        pass

    @abstractmethod
    def exists_by_name(self, name):
        pass

    @abstractmethod
    def exists_by_domain(self, domain):
        pass

    @abstractmethod
    def exists_by_email(self, email):
        pass

    @abstractmethod
    def get_by_id(
        self,
        university_id: str,
    ):
        pass
