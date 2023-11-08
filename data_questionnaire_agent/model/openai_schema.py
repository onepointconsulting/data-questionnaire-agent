from typing import List, Optional, Union

from pydantic import Field

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ResponseQuestions(BaseModel):
    """Contains the questions used to gather information to be able to give a customer advice"""

    questions: List[str] = Field(
        ...,
        description="The list of questions given used to gather information to be able to give a customer advice.",
    )

    def __str__(self) -> str:
        return "\n".join(self.questions)


class ResponseTags(BaseModel):
    """Contains information about the answer given by the user"""

    has_questions: bool = Field(
        ...,
        description="Whether the text with the answers contains embedded questions or not.",
    )
    sounds_confused: bool = Field(
        ...,
        description="Whether the text with the answers suggests that the user is confused.",
    )
    extracted_questions: Union[List[str], None] = Field(
        ...,
        description="If the text with the answers contains questions, these are the questions.",
    )
    questions_related_to_data_analytics: bool = Field(
        ...,
        description="True only if any questions are related to data analytics, data governance or data systems.",
    )


class ConditionalAdvice(BaseModel):
    """If there is enough information to give advice then advice will be available here."""

    has_advice: bool = Field(
        ...,
        description="Whether there is advice here or not",
    )
    advices: Optional[List[str]] = Field(
        ...,
        description="In case there is enough information to give advice, this list will contain advice to give to the user",
    )

    def to_html(self) -> str:
        html = "<ul>"
        for advice in self.advices:
            html += f'<li class="onepoint-blue">{advice}</li>'
        html += "</ul>"
        return html

    def __str__(self) -> str:
        return "\n\n".join(self.advices) if self.advices is not None else ""
