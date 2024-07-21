from copy import deepcopy
from pathlib import Path

from langchain.docstore.document import Document
from pydantic.v1 import BaseModel
from PySide6.QtCore import QObject, Signal

from source.models.model import Model, ModelName


class Pdf(BaseModel):
    filename: str
    path: Path
    documents: list[Document]
    metadata: dict
    summaries: dict | None


class PdfModels(Model):
    """Model class to store all loaded PDF datas"""

    data_added = Signal(str)
    summaries_added = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._pdf_data: dict[str, Pdf] = {}

    @staticmethod
    def name() -> str:
        return ModelName.PDF_DATA_MODEL.name

    @property
    def data(self):
        return deepcopy(self._pdf_data)

    @data.setter
    def data(self, value: dict[str, Pdf]):
        self._pdf_data = value

    def append_data(self, key: str, value: Pdf):
        # TODO: HS: 4.7.2024
        # Change to Pdf object
        self._pdf_data[key] = value
        self.data_added.emit(key)

    def add_summaries(self, key: str, summaries: dict):
        self._pdf_data[key].summaries = summaries
        self.summaries_added.emit(summaries["output_text"])

    def get_pdf_obj(self, key: str):
        return deepcopy(self._pdf_data.get(key, None))

    def count(self) -> int:
        return len(self._pdf_data)
