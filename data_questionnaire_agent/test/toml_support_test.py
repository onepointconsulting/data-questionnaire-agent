from data_questionnaire_agent.toml_support import DEFAULT_LANGUAGE, get_prompts


def test_english_prompt():
    prompts = get_prompts(DEFAULT_LANGUAGE)
    assert prompts is not None, "Could not find prompts"
    questionnaire = prompts["questionnaire"]
    assert questionnaire is not None, "Cannot find questionnaire"
    initial = questionnaire["initial"]
    assert initial is not None, "Cannot find initial"
