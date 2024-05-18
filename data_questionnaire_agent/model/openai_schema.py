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
        description="A lista de perguntas fornecidas usada para coletar informações para poder aconselhar um cliente.",
    )

    def __str__(self) -> str:
        return "\n".join(self.questions)


class ResponseTags(BaseModel):
    # XXX: """Contém informações sobre a resposta dada pelo usuário"""

    has_questions: bool = Field(
        ...,
       description="Se o texto com as respostas contém perguntas incorporadas ou não.",
    )
    sounds_confused: bool = Field(
        ...,
        description="Se o texto com as respostas sugere que o usuário está confuso.",
    )
    extracted_questions: Union[List[str], None] = Field(
        ...,
        description="Se o texto com as respostas contiver perguntas, estas são as perguntas.",
    )
    questions_related_to_data_analytics: bool = Field(
        ...,
        description="Verdadeiro apenas se alguma dúvida estiver relacionada à análise de dados, governança de dados ou sistemas de dados.",
    )


class ConditionalAdvice(BaseModel):
    # XXX: """Se houver informações suficientes para dar conselhos, então os conselhos estarão disponíveis aqui."""

    has_advice: bool = Field(
        ...,
        description="Se há conselhos aqui ou não",
    )
    advices: Optional[List[str]] = Field(
        ...,
        description="Caso haja informações suficientes para aconselhar, esta lista conterá conselhos a dar ao usuário",
    )
    what_you_should_avoid: Optional[List[str]] = Field(
        ...,
        description="Caso haja informações suficientes, esta lista conterá conselhos a dar ao usuário para ele evitar",
    )

    def to_html(self) -> str:
        html = "<ul>"
        for advice in self.advices:
            html += f'<li class="onepoint-blue onepoint-advice">{advice}</li>'
        html += "</ul>"
        return html
    
    def to_markdown(self) -> str:
        markdown = ""
        for advice in self.advices:
            markdown += f"- {advice}\n"
        return markdown

    def __str__(self) -> str:
        return "\n\n".join(self.advices) if self.advices is not None else ""
