from abc import ABC, abstractmethod
from management.dal import DAL


class AbstractRequestHandler(ABC):

    def __init__(self):
        self.dal = DAL()

    def __del__(self):
        del self.dal

    @abstractmethod
    def handle_request(self, data=None):
        pass
