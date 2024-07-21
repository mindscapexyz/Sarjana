from source.models.paths_model import PathsModel
from source.models.pdf_data_model import PdfModels
from source.models.prompt_model import PromptModel


class ModelStore:
    """The singleton class for all shared models"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ModelStore, cls).__new__(cls)
            cls._models = {}
            cls._models[PathsModel.name()] = PathsModel()
            cls._models[PdfModels.name()] = PdfModels()
            cls._models[PromptModel.name()] = PromptModel()

        return cls.instance

    def __setattr__(self, *_):
        raise RuntimeError("Attribute setting not allowed after model store instantiation.")

    @classmethod
    def destroy(cls):
        del cls.instance

    def paths(self) -> PathsModel:
        return self._models[PathsModel.name()]

    # TODO: HS: 2.7.2024
    # Need to store default path

    def pdf(self) -> PdfModels:
        return self._models[PdfModels.name()]

    # TODO: HS: 2.7.2024
    # Need library row column data store
    # Need credentials API data store

    def prompt(self) -> PromptModel:
        return self._models[PromptModel.name()]
