from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from langchain.chains import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate

from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.config import cfg


def prompt_factory_conditional_advice(language: str) -> ChatPromptTemplate:
    section = get_prompts(language)["advice"]
    return prompt_factory_generic(
        section,
        ["knowledge_base", "questions_answers"],
    )


def chain_factory_advice(language: str) -> LLMChain:
    return create_structured_output_chain(
        ConditionalAdvice,
        cfg.llm,
        prompt_factory_conditional_advice(language),
        verbose=cfg.verbose_llm,
    )


def prepare_conditional_advice(knowledge_base: str, questions_answers: str) -> dict:
    return {"knowledge_base": knowledge_base, "questions_answers": questions_answers}
