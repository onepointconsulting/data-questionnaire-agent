from langchain.chains import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.ontology_schema import Ontology
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts

PARAM_QUESTIONS_ANSWERS = "questions_answers"
PARAM_ADVICE = "conditional_advice"


def prompt_factory_ontology(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = get_prompts(language)
    section = prompts["extract_ontology"]
    return prompt_factory_generic(
        section=section,
        input_variables=[PARAM_ADVICE, PARAM_QUESTIONS_ANSWERS],
        prompts=prompts,
    )


def chain_factory_ontology(language: str) -> LLMChain:
    return create_structured_output_chain(
        Ontology,
        cfg.llm,
        prompt_factory_ontology(language),
        verbose=cfg.verbose_llm,
    )


def prepare_ontology_chain_call(
    questionnaire: Questionnaire, conditional_advice: ConditionalAdvice
) -> dict:
    return {
        PARAM_QUESTIONS_ANSWERS: str(questionnaire),
        PARAM_ADVICE: str(conditional_advice),
    }


async def create_ontology(
    questionnaire: Questionnaire, conditional_advice: ConditionalAdvice, language: str
) -> Ontology:
    assert conditional_advice is not None, "Missing conditional advice"
    assert questionnaire is not None, "Missing questionnaire"
    call_params = prepare_ontology_chain_call(questionnaire, conditional_advice)
    chain = chain_factory_ontology("en")
    return await chain.arun(call_params)
