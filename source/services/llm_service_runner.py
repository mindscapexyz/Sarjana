from PySide6.QtCore import QRunnable

from source.models.pdf_data_model import Pdf
from source.services.services import Services


class LLMServiceRunner(QRunnable):

    def __init__(self, pdf: Pdf):
        super().__init__()
        self._pdf = pdf

    def run(self):
        summaries = Services().llm().progressive_summarize(self._pdf.documents)
        Services().pdf().update_summaries(self._pdf.path.name, summaries)
