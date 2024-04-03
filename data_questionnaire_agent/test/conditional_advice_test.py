from data_questionnaire_agent.test.provider.advice_provider import create_simple_advice
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


def test_create_markdown():
    advice = create_simple_advice()
    markdown = advice.to_markdown()
    assert "- Monitor data quality metrics" in markdown
    print(markdown)
    advice_json = advice.json()
    assert advice_json is not None
    conditional_advice_check = ConditionalAdvice.parse_raw(advice_json)
    assert conditional_advice_check is not None
    assert len(conditional_advice_check.advices) == len(
        advice.advices
    ), "Advices lengths do not match"
