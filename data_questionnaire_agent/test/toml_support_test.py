from data_questionnaire_agent.toml_support import read_prompts_toml


def test_read_prompts_toml():
    prompts_config = read_prompts_toml()
    assert prompts_config is not None
    assert prompts_config["questionnaire"] is not None
    assert prompts_config["questionnaire"]["initial"] is not None
