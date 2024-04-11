from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chains import LLMChain

from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import prompts
from data_questionnaire_agent.config import cfg


def prompt_factory_secondary_questions() -> ChatPromptTemplate:
    section = prompts["questionnaire"]["secondary"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "questions_answers",
            "answers",
            "questions_per_batch",
        ],
    )


def chain_factory_secondary_question() -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_secondary_questions(),
        verbose=cfg.verbose_llm,
    )


def prepare_secondary_question(
    questionnaire: Questionnaire,
    knowledge_base: str,
    questions_per_batch: int = cfg.questions_per_batch,
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "questions_answers": str(questionnaire),
        "answers": questionnaire.answers_str(),
        "questions_per_batch": questions_per_batch,
    }


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )
    from data_questionnaire_agent.test.provider.knowledge_base_provider import (
        provide_data_quality_ops,
    )
    from data_questionnaire_agent.log_init import logger
    from langchain_community.callbacks import get_openai_callback
    import asyncio

    questionnaire = create_questionnaire_2_questions()
    knowledge_base = provide_data_quality_ops()
    input = prepare_secondary_question(questionnaire, knowledge_base)
    with get_openai_callback() as cb:
        chain = chain_factory_secondary_question()
        res: ResponseQuestions = asyncio.run(chain.arun(input))
        logger.info("total cost: %s", cb)
    assert isinstance(res, ResponseQuestions)
    logger.info("response questions: %s", res)
