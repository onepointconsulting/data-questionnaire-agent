from typing import Union

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.context import Context
from data_questionnaire_agent.service.graphrag_service import graphrag_context

docsearch = None


async def fetch_context(questionnaire: Union[str, Questionnaire]) -> Context:
    global docsearch

    try:
        questionnaire_str = (
            str(questionnaire)
            if isinstance(questionnaire, Questionnaire)
            else questionnaire
        )
        if cfg.use_graphrag:
            knowledge_base = await graphrag_context(questionnaire_str)
            if knowledge_base is None:
                raise Context(
                    entities_context=[],
                    relations_context=[],
                    text_units_context=[],
                    context_text="",
                )
            return knowledge_base
        else:
            raise NotImplementedError("Vector search is not supported.")
    except Exception as e:
        logger.exception("Could not fetch context.")
        logger.error(str(e))
        return Context(
            entities_context=[],
            relations_context=[],
            text_units_context=[],
            context_text="",
        )
