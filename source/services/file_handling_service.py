import json
import os
from pathlib import Path

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName


class FileHandlingService(Service):
    """Service to handle files in filesystem"""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def name() -> str:
        return ServiceName.FILE_HANDLING_SERVICE.name

    def save_pdf_obj_as_json(self, pdf_filename: str, pdf_obj: Pdf):
        pdf_filename = pdf_filename.split(".")[0] + ".json"
        path = ModelStore().paths().pdf_dir() / pdf_filename
        with open(path, "w") as w:
            w.write(pdf_obj.json())

    def load_json_into_pdf_obj(self, json_path: Path):
        with open(json_path) as j:
            dict_item = json.load(j)

        return Pdf(**dict_item)

    def read_all_local_pdf_json(self) -> list[Pdf]:
        list_pdf_obj = []
        for file in os.listdir(ModelStore().paths().pdf_dir()):
            if file.endswith(".json"):
                pdf_item = self.load_json_into_pdf_obj(ModelStore().paths().pdf_dir() / file)
                list_pdf_obj.append(pdf_item)
        return list_pdf_obj
    
    def check_file_exist(self,file:Path)-> bool:
        if file.exists():
            return True
        return False

    def delete_file(self,file:Path) -> None:
        try:
            file.unlink()
        except FileNotFoundError:
            print("File Does Not Exist")
