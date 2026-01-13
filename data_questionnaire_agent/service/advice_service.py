from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.deep_research import DeepResearchOutputs
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.persistence_service_prompt_async import get_prompts
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)


async def _prompt_factory_conditional_advice(language: str) -> ChatPromptTemplate:
    prompts = await get_prompts(language)
    section = prompts["advice"]
    return prompt_factory_generic(
        section=section,
        input_variables=["knowledge_base", "questions_answers"],
        prompts=prompts,
    )


async def chain_factory_advice(language: str) -> RunnableSequence:
    return await create_structured_question_call(language)


async def create_structured_question_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ConditionalAdvice)
    prompt = await _prompt_factory_conditional_advice(language)
    return prompt | model


def prepare_conditional_advice(knowledge_base: str, questions_answers: str) -> dict:
    return {"knowledge_base": knowledge_base, "questions_answers": questions_answers}


def combine_advices_and_deep_research_outputs(
    advices: ConditionalAdvice, deep_research_outputs: DeepResearchOutputs
) -> ConditionalAdvice:
    for advice in advices.advices:
        for deep_research_output in deep_research_outputs.outputs:
            if advice == deep_research_output.advice:
                advices.advices_with_deep_research.append(
                    (advice, deep_research_output)
                )
                break
    return advices
