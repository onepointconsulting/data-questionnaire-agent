from data_questionnaire_agent.model.session_configuration import (
    ChatType,
    SessionProperties,
)


def create_session_properties() -> SessionProperties:
    return SessionProperties(
        session_steps=6, session_language="en", chat_type=ChatType.DIVERGING
    )


def create_session_properties_to_the_point() -> SessionProperties:
    return SessionProperties(
        session_steps=6, session_language="en", chat_type=ChatType.TO_THE_POINT
    )
