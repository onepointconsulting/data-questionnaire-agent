import pytest

from data_questionnaire_agent.model.ontology_schema import Ontology
from data_questionnaire_agent.service.ontology_service import (
    create_structured_question_call,
    prepare_ontology_chain_call,
)
from data_questionnaire_agent.test.provider.advice_provider import (
    create_advice_with_questionnaire,
)


@pytest.mark.asyncio
async def test_chain_factory_ontology():
    chain = await create_structured_question_call("en")
    assert chain is not None
    conditional_advice, questionnaire = create_advice_with_questionnaire()
    assert conditional_advice is not None
    assert questionnaire is not None
    call_params = prepare_ontology_chain_call(questionnaire, conditional_advice)
    res = await chain.ainvoke(call_params)
    assert res is not None
    assert isinstance(res, Ontology)
    assert len(res.relationships) > 0
    with open("relationships.json", "w") as f:
        f.write(res.json())
