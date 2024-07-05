from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts


def prompt_factory_conditional_advice(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = get_prompts(language)
    section = prompts["advice"]
    return prompt_factory_generic(
        section=section,
        input_variables=["knowledge_base", "questions_answers"],
        prompts=prompts,
    )


def chain_factory_advice(language: str) -> LLMChain:
    return create_structured_output_chain(
        ConditionalAdvice,
        cfg.llm,
        prompt_factory_conditional_advice(language),
        verbose=cfg.verbose_llm,
    )


def create_structured_question_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ConditionalAdvice)
    prompt = prompt_factory_conditional_advice(language)
    return prompt | model


def prepare_conditional_advice(knowledge_base: str, questions_answers: str) -> dict:
    return {"knowledge_base": knowledge_base, "questions_answers": questions_answers}
