import datetime
from typing import List

from pydantic import BaseModel, Field


class Citation(BaseModel):
    index: int = Field(..., description="The index of the citation")
    title: str = Field(..., description="The text of the citation")
    url: str = Field(..., description="The url of the citation")
    start_index: int = Field(
        ..., description="The start index of the citation in the deep research output"
    )
    end_index: int = Field(
        ..., description="The end index of the citation in the deep research output"
    )
    text: str | None = Field(default=None, description="The text of the citation")

    def to_markdown(self) -> str:
        return f"""### {self.title}
[{self.url}]({self.url})
{self.start_index} - {self.end_index}
"""

    def __eq__(self, other):
        if not isinstance(other, Citation):
            return NotImplemented
        return (
            self.index == other.index
            and self.title == other.title
            and self.url == other.url
            and self.start_index == other.start_index
            and self.end_index == other.end_index
            and self.text == other.text
        )

    def __hash__(self):
        return hash((
            self.index,
            self.title,
            self.url,
            self.start_index,
            self.end_index,
            self.text,
        ))


class DeepResearchAdviceOutput(BaseModel):
    advice: str = Field(..., description="The advice")
    deep_research_output: str = Field(..., description="The deep research output")
    citations: List[Citation] = Field(..., description="The citations")


class DeepResearchOutputs(BaseModel):
    outputs: List[DeepResearchAdviceOutput] = Field(..., description="The deep research outputs")


class DeepResearchStatus(BaseModel):
    status: str = Field(..., description="The status")
    advice: str = Field(..., description="The advice")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, description="The timestamp")
