from data_questionnaire_agent.model.session_configuration import (
    SESSION_STEPS_CONFIG_KEY,
)
from data_questionnaire_agent.test.provider.session_configuration_provider import (
    create_session_configuration,
)


def test_session_configuration():
    session_configuration = create_session_configuration()
    assert session_configuration.config_key == SESSION_STEPS_CONFIG_KEY
