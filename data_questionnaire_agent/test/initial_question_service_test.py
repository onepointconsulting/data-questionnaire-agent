import asyncio

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
)
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.toml_support import get_prompts_object


def test_initial_question():
    language = "en"
    initial_question = get_prompts_object(language).questionnaire["initial"]["question"]
    assert initial_question is not None

    answer = "Data Quality"
    search_res = asyncio.run(fetch_context(answer))
    input = prepare_initial_question(
        question=initial_question,
        answer=answer,
        questions_per_batch=1,
        knowledge_base=search_res,
    )
    chain = chain_factory_initial_question("en")
    res: dict = chain.invoke(input)
    assert res is not None
    response_questions: ResponseQuestions = res["function"]

    logger.info("Results: ")
    logger.info(response_questions)
