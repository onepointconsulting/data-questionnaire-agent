from typing import List, Optional, Union

from pydantic import Field

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ResponseQuestions(BaseModel):
    # XXX: """Contém as perguntas usadas para coletar informações para poder aconselhar um cliente"""

    questions: List[str] = Field(
        ...,
        description="The list of questions given used to gather information to be able to give a customer advice.",
    )

    def __str__(self) -> str:
        return "\n".join(self.questions)


class ResponseTags(BaseModel):
    # XXX: """Contém informações sobre a resposta dada pelo usuário"""

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
    # XXX: """Se houver informações suficientes para dar conselhos, então os conselhos estarão disponíveis aqui."""

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
            html += f'<li class="onepoint-blue onepoint-advice">{advice}</li>'
        html += "</ul>"
        return html

    def __str__(self) -> str:
        return "\n\n".join(self.advices) if self.advices is not None else ""
