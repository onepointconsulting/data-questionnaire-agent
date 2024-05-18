from typing import List, Any, Union

from pydantic import BaseModel, Field
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.session_configuration import SessionConfiguration
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_markdown_bold_with_links,
)


class ServerMessage(BaseModel):
    session_id: str = Field(..., description="The application's source identifier")
    question: str = Field(..., description="The question")
    answer: str = Field(
        default="", description="The answer to the question. Should come from the user"
    )
    final_report: bool = Field(
        default=False,
        description="Whether the question is to be seen as a final report",
    )
    suggestions: List[Any] = Field(
        default=[], description="The list of suggested responses"
    )


class ServerMessages(BaseModel):
    session_id: str = Field(..., description="The application's source identifier")
    server_messages: List[ServerMessage] = Field(
        ..., description="A list with server messages"
    )
    session_configuration: Union[SessionConfiguration, None] = Field(
        default=None, description="The session configuration"
    )


def assert_server_messages_factory(questionnaire: List[QuestionnaireStatus]):
    assert questionnaire is not None, "The questionnaire is none"
    assert len(questionnaire) > 0, "Questionnaire is empty"


def convert_questionnaire(
    questionnaire: List[QuestionnaireStatus],
) -> List[ServerMessage]:
    return [
        ServerMessage(
            session_id=q.session_id,
            question=q.question,
            answer="" if q.answer is None else q.answer,
            final_report=q.final_report,
        )
        for q in questionnaire
    ]


def server_messages_factory(questionnaire: List[QuestionnaireStatus]) -> ServerMessages:
    assert_server_messages_factory(questionnaire)
    session_id = questionnaire[0].session_id
    if len(questionnaire) > 1:
        for qs in questionnaire:
            if qs.final_report:
                qs.question = replace_markdown_bold_with_links(qs.question)

    return ServerMessages(
        session_id=session_id,
        server_messages=convert_questionnaire(questionnaire),
    )
