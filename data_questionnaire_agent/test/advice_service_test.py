from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.advice_service import (
    chain_factory_advice,
    prepare_conditional_advice,
)
from data_questionnaire_agent.test.provider.knowledge_base_provider import (
    provide_knowledge_base,
)
from data_questionnaire_agent.test.provider.question_answers_provider import (
    provide_dummy_questionnaire,
)


def create_chain():
    chain = chain_factory_advice("en")
    assert chain is not None
    return chain


def test_has_advice_questionnaire():
    chain = create_chain()
    knowledge_base = provide_knowledge_base()
    questions_answers = provide_dummy_questionnaire()
    conditional_advice_input = prepare_conditional_advice(
        knowledge_base, questions_answers
    )
    res: ConditionalAdvice = chain.invoke(conditional_advice_input)
    assert res.has_advice is True, f"{res}"
    print("************ ADVICE ***************")
    print(res.to_html())
