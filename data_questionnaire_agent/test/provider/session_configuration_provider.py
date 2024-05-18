from data_questionnaire_agent.model.session_configuration import (
    SessionConfigurationEntry,
    SESSION_STEPS_CONFIG_KEY,
    DEFAULT_SESSION_STEPS,
)


def create_session_configuration():
    return SessionConfigurationEntry(
        session_id="test_id",
        config_key=SESSION_STEPS_CONFIG_KEY,
        config_value=str(DEFAULT_SESSION_STEPS),
    )
