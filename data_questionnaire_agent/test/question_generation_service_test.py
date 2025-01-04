import asyncio

import pytest
from langchain_community.callbacks import get_openai_callback

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.model.session_configuration import (
    ChatType,
    SessionProperties,
)
from data_questionnaire_agent.service.question_generation_service import (
    chain_factory_secondary_question,
    create_structured_question_call,
    divergent_prompt_transformer,
    prepare_secondary_question,
    prompt_factory_recreate_question,
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


def test_question_generation_en():
    questionnaire = (
        create_questionnaire_2_questions()
        if "refugee" not in str(cfg.raw_text_folder)
        else create_questionnaire_2_questions_refugees()
    )
    knowledge_base = provide_knowledge_base()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    with get_openai_callback() as cb:
        chain = chain_factory_secondary_question(
            SessionProperties(
                session_steps=6, session_language="en", chat_type=ChatType.DIVERGING
            )
        )
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


def test_question_regeneration_new_en():
    session_properties = create_session_properties()
    runnable = create_structured_question_call(session_properties, is_recreate=True)
    questionnaire = create_questionnaire_2_questions()
    knowledge_base = provide_knowledge_base()
    input = prepare_secondary_question(
        questionnaire, knowledge_base, questions_per_batch=1, is_recreate=True
    )
    res: ResponseQuestions = asyncio.run(runnable.ainvoke(input))
    assert isinstance(res, ResponseQuestions)
    previous_question = questionnaire.questions[-1].question
    assert len(res.questions) == 1, "Expected question length is not 1"
    assert res.questions[0] != previous_question, "The question is the same"


def test_divergent_prompt_transformer() -> str:
    prompts = get_prompts("en")
    human_message = prompts["questionnaire"]["secondary"]["human_message"]
    transformed = divergent_prompt_transformer(human_message, "en")
    assert "Main questionnaire topic:" not in transformed
    assert (
        "The questions should explore topics related to the main topic"
        not in transformed
    )


def test_prompt_factory_recreate_question():
    session_properties = SessionProperties(
        session_steps=6, session_language="en", chat_type=ChatType.TO_THE_POINT
    )
    chat_prompt_template = prompt_factory_recreate_question(session_properties)
    assert chat_prompt_template is not None, "There is no chat prompt template"
    assert (
        chat_prompt_template.messages is not None
    ), "There are no messages in the prompt template"
    assert (
        len(chat_prompt_template.messages) == 4
    ), "The template does not have the 4 expected messages"
    main_message = chat_prompt_template.messages[1]
    assert main_message.prompt is not None, "The main message does not have a prompt"
    prompt = main_message.prompt
    assert "{previous_question}" in prompt.template, "Cannot find {previous_question}"
    assert (
        "previous_question" in prompt.input_variables
    ), "previous_question parameter not found"


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
