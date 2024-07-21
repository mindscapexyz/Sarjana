from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class Author(BaseModel):
    full_name: str = Field(description="Author's full name", pattern=r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$")


class ResearchPaperMetadata(BaseModel):
    title: str = Field(description="Paper title", pattern=r"^[A-Z][A-Za-z0-9\s:,&-]{5,199}$")
    authors: List[Author] = Field(description="List of authors")
    year: int = Field(description="Year of publication", ge=1900, le=2100)
    citations: int = Field(description="Number of citations", ge=0)
    abstract: str = Field(description="Paper abstract")


class ResearchPaperList(BaseModel):
    papers: List[ResearchPaperMetadata] = Field(description="List of research papers")
