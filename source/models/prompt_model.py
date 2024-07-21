from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from PySide6.QtCore import QObject

from source.models.model import Model, ModelName
from source.models.research_paper_item_model import ResearchPaperMetadata


class PromptModel(Model):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._pdf_parser = JsonOutputParser(pydantic_object=ResearchPaperMetadata)

        self._extract_pdf_metadata_prompt = PromptTemplate(
            template="""Extract the research paper title, authors, year of research published, 
            number of citations and its abstract
        
        {format_instructions}
        
        {research_paper_contents}

        Only respond in the correct format, do not include additional properties in the JSON.\n""",
            input_variables=["research_paper_contents"],
            partial_variables={"format_instructions": self._pdf_parser.get_format_instructions()},
        )

    @property
    def pdf_metadata(self) -> PromptTemplate:
        return self._extract_pdf_metadata_prompt

    @property
    def pdf_parser(self):
        return self._pdf_parser

    @staticmethod
    def name():
        return ModelName.PROMPT_MODEL.name
