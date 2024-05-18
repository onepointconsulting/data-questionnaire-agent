from typing import List

from tenacity import AsyncRetrying

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
    convert_to_question_answers,
)
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
    similarity_search,
)
from data_questionnaire_agent.config import cfg

from data_questionnaire_agent.service.question_generation_service import (
    chain_factory_secondary_question,
    prepare_secondary_question,
)
from data_questionnaire_agent.model.openai_schema import (
    ResponseQuestions,
)

docsearch = init_vector_search()

secondary_question_chain = chain_factory_secondary_question()


async def process_secondary_questions(
    questionnaire: Questionnaire, question_per_batch: int
) -> List[QuestionAnswer]:
    knowledge_base = similarity_search(
        docsearch, questionnaire.answers_str(), how_many=cfg.search_results_how_many
    )
    secondary_question_input = prepare_secondary_question(
        questionnaire, knowledge_base, question_per_batch
    )

    async for attempt in AsyncRetrying(**cfg.retry_args):
        with attempt:
            response_questions: ResponseQuestions = await secondary_question_chain.arun(
                secondary_question_input
            )
            return convert_to_question_answers(response_questions)
