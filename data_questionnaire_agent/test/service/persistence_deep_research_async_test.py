import pytest

from data_questionnaire_agent.model.deep_research import DeepResearchAdviceOutput
from data_questionnaire_agent.service.persistence_deep_research_async import (
    save_deep_research, 
    read_deep_research, 
    delete_deep_research,
)

@pytest.mark.asyncio
async def test_save_and_read_deep_research():
    with open("data/deep_research_output.json", "r", encoding="utf-8") as f:
        deep_research_output = DeepResearchAdviceOutput.model_validate_json(f.read())
    test_session_id = "test_session_id"
    created_id = await save_deep_research(test_session_id, "test_advice", deep_research_output)
    assert created_id is not None
    saved_deep_research = await read_deep_research(test_session_id)
    assert saved_deep_research is not None
    assert len(saved_deep_research) == 1
    assert saved_deep_research[0].deep_research_output == deep_research_output.deep_research_output
    assert saved_deep_research[0].citations == deep_research_output.citations
    deleted_count = await delete_deep_research(test_session_id)
    assert deleted_count == 1
    saved_deep_research = await read_deep_research(test_session_id)
    assert saved_deep_research == []