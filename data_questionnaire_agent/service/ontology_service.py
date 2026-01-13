from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.ontology_schema import Ontology
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.persistence_service_prompt_async import get_prompts
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)


PARAM_QUESTIONS_ANSWERS = "questions_answers"
PARAM_ADVICE = "conditional_advice"


async def prompt_factory_ontology(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = await get_prompts(language)
    assert (
        "extract_ontology" in prompts
    ), "Make sure that you have the ontolgy prompt in your prompts file."
    section = prompts["extract_ontology"]
    return prompt_factory_generic(
        section=section,
        input_variables=[PARAM_ADVICE, PARAM_QUESTIONS_ANSWERS],
        prompts=prompts,
    )


async def create_structured_question_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(Ontology)
    prompt = await prompt_factory_ontology(language)
    return prompt | model


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
    chain = await create_structured_question_call(language)
    return await chain.ainvoke(call_params)
