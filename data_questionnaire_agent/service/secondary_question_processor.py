import asyncio

from tenacity import AsyncRetrying

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import (
    Questionnaire,
    QuestionnaireWithContextDocuments,
    convert_to_question_answers,
)
from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.model.context_documents import ContextDocuments
from data_questionnaire_agent.model.openai_schema import (
    ResponseQuestions,
)
from data_questionnaire_agent.model.session_configuration import SessionProperties
from data_questionnaire_agent.service.context_service import extract_relevant_documents
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.service.persistence_service_async import (
    check_question_exists,
)
from data_questionnaire_agent.service.question_generation_service import (
    create_structured_question_call,
    prepare_secondary_question,
)


MOST_COMMON_COUNT = 3


async def process_secondary_questions(
    questionnaire: Questionnaire,
    question_per_batch: int,
    session_properties: SessionProperties,
    session_id: str,
    confidence_rating: ConfidenceRating | None,
) -> QuestionnaireWithContextDocuments:
    knowledge_base = await fetch_context(questionnaire)
    secondary_question_input = prepare_secondary_question(
        questionnaire,
        knowledge_base,
        question_per_batch,
        confidence_rating=confidence_rating,
    )
    relevant_documents = extract_relevant_documents(knowledge_base, most_common_count=cfg.relevant_documents_count) if cfg.relevant_documents_count > 0 else ContextDocuments(documents=[])
    retries = 3
    while retries > 0:
        retries -= 1
        async for attempt in AsyncRetrying(**cfg.retry_args):
            with attempt:
                chain = await create_structured_question_call(session_properties)
                response_questions: ResponseQuestions = await chain.ainvoke(
                    secondary_question_input
                )
                tasks = [
                    check_question_exists(response_question, session_id)
                    for response_question in response_questions.questions
                ]
                results = await asyncio.gather(*tasks)
                has_repeated = any(results)
                if not has_repeated or retries == 0:
                    questionnaire = Questionnaire(
                        questions=convert_to_question_answers(response_questions)
                    )
                    return QuestionnaireWithContextDocuments(
                        questionnaire=questionnaire,
                        context_documents=relevant_documents,
                    )
    # Fallback: if all retries failed, return empty list with relevant_documents
    # This should ideally not happen, but ensures the function always returns a tuple
    return QuestionnaireWithContextDocuments(
        questionnaire=Questionnaire(questions=[]), context_documents=relevant_documents
    )
