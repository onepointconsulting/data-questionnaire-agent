from data_questionnaire_agent.service.report_aggregation_summarization_service import (
    prompt_factory_summarization_prompt,
    create_summarization_call
)


def test_prompt_factory_summarization_prompt():
    chat_template = prompt_factory_summarization_prompt("en")
    assert chat_template is not None, "Chat template cannot be none"
    res = chat_template.format(full_questionnaire="Bla")
    assert res is not None, "No result from formatting"


def test_create_summarization_call():
    runnable = create_summarization_call("en")
    assert runnable is not None, "Runnable is none"