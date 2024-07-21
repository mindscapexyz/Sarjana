from enum import Enum, auto

from PySide6.QtCore import QObject, QReadWriteLock


class ModelName(Enum):
    """Enum for unique model name"""

    PATHS_MODEL = auto()
    PDF_DATA_MODEL = auto()
    PROMPT_MODEL = auto()


class Model(QObject):
    """Base class for a model object"""

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self._lock = QReadWriteLock(QReadWriteLock.RecursionMode.Recursive)

    def lock(self) -> QReadWriteLock:
        return self._lock

    @staticmethod
    def name():
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        if cls.name == Model.name:
            raise TypeError("Subclasses of `Model` must override the name method")
        return super().__init_subclass__()
