import pytest
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.service.add_more_suggestions_service import (
    chain_factory_add_more_suggestions,
    prompt_factory_add_more_suggestions,
)

@pytest.mark.asyncio
async def test_add_more_suggestions_service():
    template = await prompt_factory_add_more_suggestions("en")
    assert template is not None
    for var in template.input_variables:
        assert var in [
            "knowledge_base",
            "questions_answers",
            "question",
            "suggestions",
            "confidence_report",
        ], f"Unexpected input variable: {var}"


@pytest.mark.asyncio
async def test_chain_factory_add_more_suggestions():
    chain = await chain_factory_add_more_suggestions("en")
    assert chain is not None
    assert isinstance(chain, RunnableSequence), "Chain is not a RunnableSequence"
