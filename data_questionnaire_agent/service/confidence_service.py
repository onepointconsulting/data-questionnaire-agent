from langchain.prompts import ChatPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.service.ontology_service import PARAM_QUESTIONS_ANSWERS
from data_questionnaire_agent.config import cfg


def prompt_factory_confidence(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = get_prompts(language)
    assert (
        "confidence_prompt" in prompts
    ), "Make sure that you have the confidence prompt in your prompts file."
    section = prompts["confidence_prompt"]
    return prompt_factory_generic(
        section=section,
        input_variables=[PARAM_QUESTIONS_ANSWERS],
        prompts=prompts,
    )


def create_structured_question_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ConfidenceRating)
    prompt = prompt_factory_confidence(language)
    return prompt | model


def prepare_confidence_chain_call(questionnaire: Questionnaire) -> dict:
    return {PARAM_QUESTIONS_ANSWERS: str(questionnaire)}


async def calculate_confidence_rating(
    questionnaire: Questionnaire, language: str
) -> ConfidenceRating:
    assert questionnaire is not None, "Missing questionnaire"
    call_params = prepare_confidence_chain_call(questionnaire)
    chain = create_structured_question_call(language)
    return await chain.ainvoke(call_params)
