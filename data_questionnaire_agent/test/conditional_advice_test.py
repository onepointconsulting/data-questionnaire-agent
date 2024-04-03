from data_questionnaire_agent.test.provider.advice_provider import create_simple_advice


def test_create_markdown():
    advice = create_simple_advice()
    markdown = advice.to_markdown()
    assert "- Monitor data quality metrics" in markdown
    print(markdown)
