import asyncio

import pytest

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.report_aggregation_summarization_service import (
    aexecute_summarization_batch,
    create_summarization_call,
    prompt_factory_summarization_prompt,
)


def test_prompt_factory_summarization_prompt():
    chat_template = prompt_factory_summarization_prompt("en")
    assert chat_template is not None, "Chat template cannot be none"
    res = chat_template.format(full_questionnaire="Bla")
    assert res is not None, "No result from formatting"


@pytest.mark.asyncio
async def test_create_summarization_call():
    runnable = await create_summarization_call("en")
    assert runnable is not None, "Runnable is none"


def test_aexecute_summarization_batch():
    files = [
        "data/sample_questionnaire1.md",
        "data/sample_questionnaire2.md",
        "data/sample_questionnaire3.md",
    ]
    texts = [(cfg.project_root / f).read_text(encoding="utf-8") for f in files]
    summaries = asyncio.run(aexecute_summarization_batch(texts))
    assert summaries is not None
    assert len(summaries) == len(files)
