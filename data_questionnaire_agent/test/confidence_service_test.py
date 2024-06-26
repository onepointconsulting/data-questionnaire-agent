from data_questionnaire_agent.service.confidence_service import prompt_factory_confidence

def test_prompt_factory_confidence():
    prompt_template = prompt_factory_confidence("en")
    assert prompt_template is not None
    assert prompt_template.messages is not None
    assert len(prompt_template.messages) > 0
