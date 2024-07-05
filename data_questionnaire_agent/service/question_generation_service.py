from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts


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


def create_structured_question_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ResponseQuestions)
    prompt = prompt_factory_secondary_questions(language)
    return prompt | model


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
