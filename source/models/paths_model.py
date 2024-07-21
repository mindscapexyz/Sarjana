import os
from pathlib import Path

from PySide6.QtCore import QObject

from source import USER_DATA_DIR
from source.models.model import Model, ModelName


class PathsModel(Model):
    """Store all the common paths"""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._pdf_dir = USER_DATA_DIR / "pdf"
        os.makedirs(self._pdf_dir, exist_ok=True)

    @staticmethod
    def name() -> str:
        return ModelName.PATHS_MODEL.name

    def pdf_dir(self) -> Path:
        return self._pdf_dir
