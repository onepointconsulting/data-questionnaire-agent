from data_questionnaire_agent.service.mail_sender import validate_address


def test_validate_address_ok():
    assert validate_address("john.doe@gmail.com")
    assert validate_address("mary.do@protonmail.com")


def test_validate_address_not_ok():
    assert not validate_address("john.doegmail.com")
    assert not validate_address("mary.doprotonmail.com")
