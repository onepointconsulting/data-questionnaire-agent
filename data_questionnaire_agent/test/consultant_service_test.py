import asyncio

import pytest

from data_questionnaire_agent.service.consultant_service import (
    convert_all_consultants,
    convert_to_markdown,
    create_structured_consultant_call,
    prepare_consultant_call,
    prompt_factory_consultants,
)
from data_questionnaire_agent.test.provider.advice_provider import create_full_advice1
from data_questionnaire_agent.test.provider.consultant_provider import (
    create_simple_consultant,
)
from data_questionnaire_agent.test.provider.questionnaire_provider import (
    create_questionnaire_7_questions,
)


def test_convert_to_markdown():
    consultant = create_simple_consultant()
    markdown = convert_to_markdown([consultant])
    assert markdown is not None, "There is no markdown"
    assert "John" in markdown, "John is not in markdown"
    assert "Doe" in markdown, "Doe is not in markdown"
    assert "gmail" in markdown, "gmail is not in markdown"


def test_convert_all_consultants():
    markdown = asyncio.run(convert_all_consultants())
    assert markdown is not None, "there is not markdown"
    from pathlib import Path

    Path("/tmp/consultants.md").write_text(markdown)


@pytest.mark.asyncio
async def test_prompt_factory_consultants():
    prompt_template = await prompt_factory_consultants("en")
    assert prompt_template is not None, "There is no prompt template"
    prompt_template.config_schema is not None, "There is no configuration schema"


@pytest.mark.asyncio
async def test_create_structured_consultant_call():
    runnable_sequence = await create_structured_consultant_call("en")
    assert runnable_sequence is not None, "There is no runnable sequence"


def provide_dummy_data():
    questionnaire = create_questionnaire_7_questions()
    advice = create_full_advice1()
    prompt_data = asyncio.run(prepare_consultant_call(questionnaire, advice))
    assert prompt_data is not None, "There is no prompt data."
    assert (
        prompt_data["questions_answers"] is not None
    ), "There are no question and answers"
    return prompt_data


def test_prepare_consultant_call():
    provide_dummy_data()


def test_call_consultant_evaluation():
    prompt_data = provide_dummy_data()
    runnable_sequence = create_structured_consultant_call("en")
    consultant_ratings = runnable_sequence.invoke(prompt_data)
    assert consultant_ratings is not None, "There are no consultant ratings"
