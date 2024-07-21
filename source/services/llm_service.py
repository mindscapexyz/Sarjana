import os
import textwrap
from pathlib import Path

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains.mapreduce import MapReduceChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName


class LlmService(Service):
    """Service to handle llm"""

    def __init__(self) -> None:
        super().__init__()

        self._api_key = os.environ["OPENAI_API_KEY"]
        self._llm = ChatOpenAI(name="gpt-3.5-turbo", api_key=self._api_key)

        self._prompt = ChatPromptTemplate.from_template("Write a short story about {topic} in {style} style.")

        self._chain = self._prompt | self._llm | StrOutputParser()

    @staticmethod
    def name() -> str:
        return ServiceName.LLM_SERVICE.name

    def invoke_dummy_llm_response(self):
        response = self._chain.invoke({"topic": "a robot learning to paint", "style": "whimsical"})
        print(response)

    def invoke_research_paper(self):
        self._chain = ModelStore().prompt().pdf_metadata | self._llm | ModelStore().prompt().pdf_parser
        dummy_input = str(
            {
                "title": "Enhancing Deep Learning Architectures: Innovations in Optimization and Generalization",
                "authors": "Alice Johnson",
                "year": 2024,
                "citations": 150,
                "abstract": "Deep learning continues to be at the forefront of the artificial intelligence revolution, driving significant breakthroughs in areas ranging from automated diagnosis to autonomous vehicle technology. This paper presents novel methodologies for enhancing the performance of deep learning architectures through advanced optimization techniques and improved generalization strategies. We introduce a new gradient descent optimization algorithm that significantly reduces convergence times and enhances the stability of training across various network architectures, including convolutional and recurrent neural networks. Additionally, we propose a novel regularization method that effectively mitigates overfitting while maintaining the model's ability to generalize from training to unseen data, thereby enhancing its applicability in real-world scenarios. We conduct extensive experiments across multiple datasets and benchmarks, demonstrating substantial improvements in performance compared to existing methods. Our study not only provides new insights into the mechanisms of deep learning optimization and generalization but also offers practical solutions that can be readily implemented in diverse applications. The implications of this research extend beyond mere academic interest, suggesting a roadmap for future development in the field of deep learning.",
            }
        )
        response = self._chain.invoke({"research_paper_contents": dummy_input})
        print(response)

    def parse_research_paper_metadata(self, text: str) -> dict:
        self._chain = ModelStore().prompt().pdf_metadata | self._llm | ModelStore().prompt().pdf_parser

        response = self._chain.invoke({"research_paper_contents": text})
        return response

    def progressive_summarize(self, docs: list[Document]) -> dict:
        # with a custom prompt

        # prompt_template = """Write a concise summary of the following:

        #     {text}

        #     CONSCISE SUMMARY IN BULLET POINTS:"""

        prompt_template = """Write a concise summary of the following:

            {text}
            
        WRITE SUMMARY IN ONE LONG PARAGRAPH"""

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(
            OpenAI(temperature=0),
            chain_type="map_reduce",
            return_intermediate_steps=True,
            map_prompt=PROMPT,
            combine_prompt=PROMPT,
        )

        output_summary = chain({"input_documents": docs}, return_only_outputs=True)
        wrapped_text = textwrap.fill(
            output_summary["output_text"], width=100, break_long_words=False, replace_whitespace=False
        )
        return output_summary
