from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chains import LLMChain

from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.config import cfg


def prompt_factory_secondary_questions(language: str) -> ChatPromptTemplate:
    prompts = get_prompts(language)
    section = prompts["questionnaire"]["secondary"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "questions_answers",
            "answers",
            "questions_per_batch",
        ],
        prompts,
    )


def chain_factory_secondary_question(language: str) -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_secondary_questions(language),
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
        create_questionnaire_2_questions_refugees,
        create_questionnaire_2_questions__refugees_fa,
    )
    from data_questionnaire_agent.test.provider.knowledge_base_provider import (
        provide_knowledge_base,
    )
    from data_questionnaire_agent.log_init import logger
    from langchain_community.callbacks import get_openai_callback
    import asyncio

    def test_en():
        questionnaire = (
            create_questionnaire_2_questions()
            if not "refugee" in str(cfg.raw_text_folder)
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

        # Farsi version

    def test_fa():
        questionnaire = (
            create_questionnaire_2_questions()
            if not "refugee" in str(cfg.raw_text_folder)
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

    # test_en()
    test_fa()
