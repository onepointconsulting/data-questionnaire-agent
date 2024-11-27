import asyncio

import pytest
from langchain_community.callbacks import get_openai_callback

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.question_generation_service import (
    chain_factory_secondary_question,
    create_structured_question_call,
    prepare_secondary_question,
)
from data_questionnaire_agent.test.provider.knowledge_base_provider import (
    provide_knowledge_base,
)
from data_questionnaire_agent.test.provider.questionnaire_provider import (
    create_questionnaire_2_questions,
    create_questionnaire_2_questions__refugees_fa,
    create_questionnaire_2_questions_refugees,
)
from data_questionnaire_agent.test.provider.session_properties_provider import (
    create_session_properties,
)
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.service.question_generation_service import divergent_prompt_transformer


def test_question_generation_en():
    questionnaire = (
        create_questionnaire_2_questions()
        if "refugee" not in str(cfg.raw_text_folder)
        else create_questionnaire_2_questions_refugees()
    )
    knowledge_base = provide_knowledge_base()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    with get_openai_callback() as cb:
        chain = chain_factory_secondary_question("en")
        res: ResponseQuestions = asyncio.run(chain.arun(input))
        logger.info("total cost: %s", cb)
    assert isinstance(res, ResponseQuestions)
    logger.info("response questions: %s", res)


def test_question_generation_new_en():
    session_properties = create_session_properties()
    runnable = create_structured_question_call(session_properties)
    questionnaire = create_questionnaire_2_questions()
    knowledge_base = provide_knowledge_base()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    res: ResponseQuestions = asyncio.run(runnable.ainvoke(input))
    assert isinstance(res, ResponseQuestions)


def test_divergent_prompt_transformer() -> str:
    prompts = get_prompts("en")
    human_message = prompts["questionnaire"]["secondary"]["human_message"]
    transformed = divergent_prompt_transformer(human_message, "en")
    assert not "Main questionnaire topic:" in transformed
    assert not "The questions should explore topics related to the main topic" in transformed


@pytest.mark.skip(reason="no way of currently testing this")
def test_question_generation_fa():
    questionnaire = (
        create_questionnaire_2_questions()
        if "refugee" not in str(cfg.raw_text_folder)
        else create_questionnaire_2_questions__refugees_fa()
    )
    knowledge_base = provide_knowledge_base()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    with get_openai_callback() as cb:
        chain = chain_factory_secondary_question("fa")
        res: ResponseQuestions = asyncio.run(chain.arun(input))
        logger.info("total cost: %s", cb)
    assert isinstance(res, ResponseQuestions)
    logger.info("response questions: %s", res)
