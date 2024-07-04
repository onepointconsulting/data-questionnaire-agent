from asyncer import asyncify
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from tenacity import AsyncRetrying

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.advice_service import (
    chain_factory_advice,
    prepare_conditional_advice,
)
from data_questionnaire_agent.service.similarity_search import similarity_search


async def process_advice(
    docsearch: FAISS, questionnaire: Questionnaire, advice_chain: LLMChain
) -> ConditionalAdvice:
    questionnaire_str = str(questionnaire)

    knowledge_base = await asyncify(similarity_search)(
        docsearch, questionnaire_str, how_many=cfg.search_results_how_many
    )
    advice_input = prepare_conditional_advice(
        knowledge_base=knowledge_base, questions_answers=questionnaire_str
    )
    async for attempt in AsyncRetrying(**cfg.retry_args):
        with attempt:
            conditional_advice: ConditionalAdvice = await advice_chain.arun(
                advice_input
            )
            if conditional_advice.has_advice:
                for advice in conditional_advice.advices:
                    logger.info(advice)
            return conditional_advice


if __name__ == "__main__":
    import asyncio

    from data_questionnaire_agent.service.similarity_search import init_vector_search
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )

    advice_chain = chain_factory_advice()
    questionnaire = create_questionnaire_2_questions()
    docsearch = init_vector_search()
    print(asyncio.run(process_advice(docsearch, questionnaire, advice_chain)))
