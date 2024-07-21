from source.services.file_handling_service import FileHandlingService
from source.services.llm_service import LlmService
from source.services.pdf_service import PdfService


class Services:
    """The singleton class for all useable services."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Services, cls).__new__(cls)
            cls._services = {}
            cls._services[PdfService.name()] = PdfService()
            cls._services[LlmService.name()] = LlmService()
            cls._services[FileHandlingService.name()] = FileHandlingService()

        return cls.instance

    @classmethod
    def destroy(cls):
        del cls.instance

    def __setattr__(self, *_):
        # No attribute setting is allowed on the Services
        raise RuntimeError("Attribute setting not allowed.")

    def pdf(self) -> PdfService:
        return self._services[PdfService.name()]

    def llm(self) -> LlmService:
        return self._services[LlmService.name()]

    def file_handling(self) -> FileHandlingService:
        return self._services[FileHandlingService.name()]
