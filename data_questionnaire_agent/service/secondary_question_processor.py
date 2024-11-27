import asyncio
from typing import List

from tenacity import AsyncRetrying

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
    convert_to_question_answers,
)
from data_questionnaire_agent.model.openai_schema import (
    ResponseQuestions,
)
from data_questionnaire_agent.model.session_configuration import SessionProperties
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.service.persistence_service_async import (
    check_question_exists,
)
from data_questionnaire_agent.service.question_generation_service import (
    create_structured_question_call,
    prepare_secondary_question,
)


async def process_secondary_questions(
    questionnaire: Questionnaire,
    question_per_batch: int,
    session_properties: SessionProperties,
    session_id: str,
) -> List[QuestionAnswer]:
    knowledge_base = await fetch_context(questionnaire)
    secondary_question_input = prepare_secondary_question(
        questionnaire, knowledge_base, question_per_batch
    )
    retries = 3
    while retries > 0:
        retries -= 1
        async for attempt in AsyncRetrying(**cfg.retry_args):
            with attempt:
                response_questions: ResponseQuestions = (
                    await create_structured_question_call(session_properties).ainvoke(
                        secondary_question_input
                    )
                )
                tasks = [
                    check_question_exists(response_question, session_id)
                    for response_question in response_questions.questions
                ]
                results = await asyncio.gather(*tasks)
                has_repeated = any(results)
                if not has_repeated or retries == 0:
                    return convert_to_question_answers(response_questions)
