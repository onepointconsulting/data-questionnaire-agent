from langchain.prompts import ChatPromptTemplate

from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.service.ontology_service import PARAM_QUESTIONS_ANSWERS


def prompt_factory_confidence(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = get_prompts(language)
    assert (
        "confidence_prompt" in prompts
    ), "Make sure that you have the confidence prompt in your prompts file."
    section = prompts["extract_ontology"]
    return prompt_factory_generic(
        section=section,
        input_variables=[PARAM_QUESTIONS_ANSWERS],
        prompts=prompts,
    )
