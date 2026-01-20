from langchain_core.runnables.base import RunnableSequence
from tenacity import AsyncRetrying

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.advice_service import (
    chain_factory_advice,
    prepare_conditional_advice,
)
from data_questionnaire_agent.service.knowledge_base_service import fetch_context


async def process_advice(
    questionnaire: Questionnaire, advice_chain: RunnableSequence
) -> ConditionalAdvice:
    questionnaire_str = str(questionnaire)

    knowledge_base = await fetch_context(questionnaire_str)

    advice_input = prepare_conditional_advice(
        knowledge_base=knowledge_base.context_text, questions_answers=questionnaire_str
    )
    async for attempt in AsyncRetrying(**cfg.retry_args):
        with attempt:
            conditional_advice: ConditionalAdvice = await advice_chain.ainvoke(
                advice_input
            )
            if conditional_advice.has_advice:
                for advice in conditional_advice.advices:
                    logger.info(advice)
            return conditional_advice


if __name__ == "__main__":
    import asyncio

    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )

    async def test_process_advice():
        advice_chain = await chain_factory_advice("en")
        questionnaire = create_questionnaire_2_questions()
        res = await process_advice(questionnaire, advice_chain)
        print(res.to_html())

    asyncio.run(test_process_advice())
