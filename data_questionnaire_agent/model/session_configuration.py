from enum import StrEnum
from typing import List, Union

from pydantic.v1 import BaseModel, Field

DEFAULT_SESSION_STEPS = 6

SESSION_STEPS_CONFIG_KEY = "session-steps"
SESSION_STEPS_LANGUAGE_KEY = "session-language"
SESSION_CHAT_TYPE = "session-chat-type"
CLIENT_ID_KEY = "session-client-id"


class ChatType(StrEnum):
    DIVERGING = "diverging"
    TO_THE_POINT = "to_the_point"


DEFAULT_CHAT_TYPE = ChatType.DIVERGING


def chat_type_factory(s: str) -> ChatType:
    try:
        return ChatType(s)
    except ValueError:
        return DEFAULT_CHAT_TYPE


class SessionConfigurationEntry(BaseModel):
    id: Union[int, None] = Field(
        default=None, description="The identifier of this session configuration"
    )
    session_id: str = Field(..., description="The application's source identifier")
    config_key: str = Field(..., description="The configuration key")
    config_value: str = Field(..., description="The configuration value")


class SessionConfiguration(BaseModel):
    configuration_entries: List[SessionConfigurationEntry] = Field(
        ..., description="All session configuration entries"
    )


class SessionProperties(BaseModel):
    session_steps: int = Field(..., description="The session steps")
    session_language: str = Field(..., description="The session language")
    chat_type: ChatType = Field(..., description="The type of the chat")


def create_session_configurations(
    session_id: str,
    session_properties: SessionProperties,
    client_id: str = "",
) -> List[SessionConfigurationEntry]:
    session_steps = session_properties.session_steps
    chat_type = session_properties.chat_type
    language = session_properties.session_language
    session_configuration_entry = SessionConfigurationEntry(
        session_id=session_id,
        config_key=SESSION_STEPS_CONFIG_KEY,
        config_value=str(session_steps),
    )
    session_configuration_language = SessionConfigurationEntry(
        session_id=session_id,
        config_key=SESSION_STEPS_LANGUAGE_KEY,
        config_value=language,
    )
    session_configuration_chat_type = SessionConfigurationEntry(
        session_id=session_id,
        config_key=SESSION_CHAT_TYPE,
        config_value=chat_type.value,
    )
    session_keys = [
        session_configuration_entry,
        session_configuration_language,
        session_configuration_chat_type,
    ]
    if client_id is not None and len(client_id.strip()) > 0:
        session_keys.append(
            SessionConfigurationEntry(
                session_id=session_id,
                config_key=CLIENT_ID_KEY,
                config_value=client_id,
            )
        )
    return session_keys
