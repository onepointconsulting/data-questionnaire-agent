from typing import Union

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.service.graphrag_service import graphrag_context
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
    similarity_search,
)
from data_questionnaire_agent.log_init import logger

docsearch = None


async def fetch_context(questionnaire: Union[str, Questionnaire]) -> str:
    global docsearch

    try:
        questionnaire_str = (
            str(questionnaire)
            if isinstance(questionnaire, Questionnaire)
            else questionnaire
        )
        if cfg.use_graphrag:
            knowledge_base = await graphrag_context(questionnaire_str)
            return knowledge_base or ""
        else:
            if docsearch is None:
                docsearch = init_vector_search()
            knowledge_base = similarity_search(
                docsearch, questionnaire_str, how_many=cfg.search_results_how_many
            )
            return knowledge_base or ""
    except Exception as e:
        logger.exception("Could not fetch context.")
        logger.error(str(e))
        return ""