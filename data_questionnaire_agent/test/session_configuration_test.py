from data_questionnaire_agent.model.session_configuration import (
    SESSION_STEPS_CONFIG_KEY,
    SESSION_STEPS_LANGUAGE_KEY,
    ChatType,
    chat_type_factory,
    create_session_configurations,
)
from data_questionnaire_agent.test.provider.session_configuration_provider import (
    create_session_configuration,
)
from data_questionnaire_agent.test.provider.session_properties_provider import (
    create_session_properties,
)


def test_session_configuration():
    session_configuration = create_session_configuration()
    assert session_configuration.config_key == SESSION_STEPS_CONFIG_KEY


def test_chat_type_factory():
    assert chat_type_factory(ChatType.DIVERGING.value) == ChatType.DIVERGING
    assert chat_type_factory(ChatType.TO_THE_POINT.value) == ChatType.TO_THE_POINT
    assert chat_type_factory("bla") == ChatType.DIVERGING


def test_create_session_configurations():
    session_properties = create_session_properties()
    config_entries = create_session_configurations(
        "12345", session_properties, "hi there"
    )
    assert len(config_entries) == 4
    assert config_entries[0].config_key == SESSION_STEPS_CONFIG_KEY
    assert config_entries[1].config_key == SESSION_STEPS_LANGUAGE_KEY
