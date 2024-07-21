import abc
from enum import Enum, auto


class ServiceName(Enum):
    """Enum for unique service names"""

    PDF_SERVICE = auto()
    LLM_SERVICE = auto()
    FILE_HANDLING_SERVICE = auto()


class Service(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass
