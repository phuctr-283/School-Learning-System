from abc import ABC, abstractmethod


class SchoolAdminRepository(ABC):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    def create(self, entity):
        raise NotImplementedError

    def find_by_email(self, email):
        raise NotImplementedError