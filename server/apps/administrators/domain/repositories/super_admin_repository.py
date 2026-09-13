from abc import ABC, abstractmethod


class SuperAdminRepository(ABC):

    @abstractmethod
    def create(self, admin):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError