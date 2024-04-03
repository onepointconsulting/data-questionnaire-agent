from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.advice_service import (
    chain_factory_advice,
    prepare_conditional_advice,
    prompt_factory_conditional_advice,
)
from data_questionnaire_agent.test.provider.knowledge_base_provider import (
    provide_data_quality_ops,
)
from data_questionnaire_agent.test.provider.question_answers_provider import (
    provide_data_silo_questionnaire,
    provide_incomplete_questionnaire,
)


def create_chain():
    chain = chain_factory_advice()
    assert chain is not None
    return chain


def test_has_advice_questionnaire():
    chain = create_chain()
    knowledge_base = provide_data_quality_ops()
    questions_answers = provide_data_silo_questionnaire()
    conditional_advice_input = prepare_conditional_advice(
        knowledge_base, questions_answers
    )
    res: ConditionalAdvice = chain.run(conditional_advice_input)
    assert res.has_advice is True


# def test_has_no_advice_questionnaire():
#     chain = create_chain()
#     knowledge_base = provide_data_quality_ops()
#     incomplete_questionnaire = provide_incomplete_questionnaire()
#     incomplete_advice_input = prepare_conditional_advice(
#         knowledge_base, incomplete_questionnaire
#     )
#     res: ConditionalAdvice = chain.run(incomplete_advice_input)
#     assert res.has_advice is False
