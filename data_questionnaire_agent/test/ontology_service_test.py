from data_questionnaire_agent.service.ontology_service import (
    chain_factory_ontology, prepare_ontology_chain_call
)
from data_questionnaire_agent.test.provider.advice_provider import (
    create_advice_with_questionnaire,
)
from data_questionnaire_agent.model.ontology_schema import Ontology
from data_questionnaire_agent.log_init import logger


def test_chain_factory_ontology():
    chain = chain_factory_ontology("en")
    assert chain is not None
    conditional_advice, questionnaire = create_advice_with_questionnaire()
    assert conditional_advice is not None
    assert questionnaire is not None
    call_params = prepare_ontology_chain_call(questionnaire, conditional_advice)
    res = chain.run(call_params)
    assert res is not None
    assert isinstance(res, Ontology)
    assert len(res.relationships) > 0
    with open("relationships.txt", "w") as f:
        for r in res.relationships:
            f.write(f"""{str(r)}

""")