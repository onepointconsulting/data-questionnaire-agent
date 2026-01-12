from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.question_suggestion import PossibleAnswers
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.service.persistence_service_async import (
    save_additional_suggestions,
    select_confidence,
    select_last_questionnaire_status_suggestions,
    select_questionnaire,
)
from data_questionnaire_agent.service.persistence_service_prompt_async import read_system_human_prompts
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts


async def prompt_factory_add_more_suggestions(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    section = await read_system_human_prompts(["questionnaire", "add_more_suggestions"], language)
    return prompt_factory_generic(
        section=section,
        input_variables=[
            "knowledge_base",
            "questions_answers",
            "question",
            "suggestions",
            "confidence_report",
        ],
        prompts=get_prompts(language),
    )


async def chain_factory_add_more_suggestions(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(PossibleAnswers)
    prompt = await prompt_factory_add_more_suggestions(language)
    return prompt | model


def prepare_add_more_suggestions(
    knowledge_base: str,
    questions_answers: str,
    question: str,
    suggestions: str,
    confidence_report: str,
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "questions_answers": questions_answers,
        "question": question,
        "suggestions": suggestions,
        "confidence_report": confidence_report,
    }


async def process_add_more_suggestions(
    session_id: str, question: str | None, language: str
) -> PossibleAnswers:
    # Gather all information use for generation
    questionnaire = await select_questionnaire(session_id)
    if not questionnaire:
        raise ValueError(f"Questionnaire with session_id {session_id} not found.")
    knowledge_base = await fetch_context(questionnaire)
    questions_answers = str(questionnaire)
    if question is None:
        question = questionnaire.questions[-1].question
    suggestions = await select_last_questionnaire_status_suggestions(session_id)
    if not suggestions:
        raise ValueError(f"No suggestions found for session_id {session_id}.")
    confidence_rating = await select_confidence(
        session_id, len(questionnaire.questions) - 1
    )
    confidence_report = confidence_rating.to_markdown() if confidence_rating else ""
    input = prepare_add_more_suggestions(
        knowledge_base=knowledge_base,
        questions_answers=questions_answers,
        question=question,
        suggestions="\n".join([f"- {s.main_text}" for s in suggestions]),
        confidence_report=confidence_report,
    )
    # Generate suggestions
    chain = await chain_factory_add_more_suggestions(language)
    result: PossibleAnswers = await chain.ainvoke(input)
    # Save the suggestions to the database
    await save_additional_suggestions(result, session_id)
    return result


if __name__ == "__main__":
    import asyncio

    def test_process_add_more_suggestions():
        session_id = "01JSKXKM2FBAZ9YMPP54X2PDW9"
        question = "What specific challenges do you face in ensuring compliance with data privacy regulations like GDPR or CCPA in your AI systems?"
        language = "en"

        asyncio.run(process_add_more_suggestions(session_id, question, language))

    test_process_add_more_suggestions()
