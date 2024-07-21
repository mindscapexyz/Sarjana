from pathlib import Path

from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from llama_index.readers.file import PyMuPDFReader
from pypdf import PdfReader
from PySide6.QtCore import Slot

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName


class PdfService(Service):
    """Service to handle PDF data"""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def name() -> str:
        return ServiceName.PDF_SERVICE.name

    def load_pdf(self, path: Path) -> list[Document]:
        pdf_loader = PyPDFLoader(str(path))
        documents = pdf_loader.load_and_split()
        return documents

    def get_first_page_pdf_text(self, pdf_path: Path) -> str:
        pdf = PdfReader(pdf_path)
        first_page = pdf.pages[0]
        contents = first_page.get_contents()
        texts = first_page.extract_text()
        print(contents)
        print(texts)
        return texts

    def append_data(self, key: str, value: Pdf):
        ModelStore().pdf().append_data(key, value)

    def update_summaries(self, key: str, value: dict):
        ModelStore().pdf().add_summaries(key, value)

    def create_pdf_obj(self, path: Path, documents: list[Document], metadata: dict):
        print(path)
        print(documents)
        print(metadata)
        return Pdf(filename=path.name, path=path, documents=documents, metadata=metadata, summaries=None)
