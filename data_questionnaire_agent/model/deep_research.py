import datetime
from typing import List

from pydantic import BaseModel, Field

from data_questionnaire_agent.model.application_schema import Questionnaire


class DeepResearchAdviceInput(BaseModel):
    questionnaire: Questionnaire = Field(..., description="The questionnaire")
    conditional_advice: str = Field(
        ...,
        description="The conditional advice which has been generated and being researched",
    )


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
