from typing import Any, List, Union

from pydantic.v1 import BaseModel, Field

from data_questionnaire_agent.model.global_configuration import GlobalConfiguration
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.session_configuration import SessionConfiguration


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
    clarification: Union[str, None] = Field(
        ..., description="The clarification or explanation of the question"
    )


class ServerMessages(BaseModel):
    session_id: str = Field(..., description="The application's source identifier")
    server_messages: List[ServerMessage] = Field(
        ..., description="A list with server messages"
    )
    session_configuration: Union[SessionConfiguration, None] = Field(
        default=None, description="The session configuration"
    )
    global_configuration: Union[GlobalConfiguration, None] = Field(
        default=None, description="The global configuration with key value pairs"
    )

class ErrorMessage(BaseModel):
    session_id: str = Field(..., description="The application's source identifier")
    error: str = Field(..., description="The error message")


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
            clarification=q.clarification,
        )
        for q in questionnaire
    ]


def server_messages_factory(questionnaire: List[QuestionnaireStatus]) -> ServerMessages:
    assert_server_messages_factory(questionnaire)
    session_id = questionnaire[0].session_id
    return ServerMessages(
        session_id=session_id,
        server_messages=convert_questionnaire(questionnaire),
    )
