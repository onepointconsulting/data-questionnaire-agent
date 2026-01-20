import chainlit as cl
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain
from tenacity import AsyncRetrying

# Activating REST interfaces
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseTags
from data_questionnaire_agent.service.tagging_service import prepare_sentiment_input


async def process_clarifications_chainlit(
    questionnaire: Questionnaire,
    questions_to_process: int,
    has_questions_chain: LLMChain,
    clarification_agent: AgentExecutor,
    use_chainlit: bool = True,
):
    questions = questionnaire.questions[-questions_to_process:]
    content = "\n".join([q.answer for q in questions])

    async for attempt in AsyncRetrying(**cfg.retry_args):
        with attempt:
            response_tags: ResponseTags = await has_questions_chain.arun(
                prepare_sentiment_input(content)
            )
            if len(response_tags.extracted_questions) > 0:
                if response_tags.questions_related_to_data_analytics:
                    for clarification_question in response_tags.extracted_questions:
                        clarification = await clarification_agent.arun(
                            clarification_question
                        )
                        if use_chainlit:
                            await cl.Message(content=clarification).send()
                        else:
                            logger.info(clarification)
                else:
                    message = f"These questions: {response_tags.extracted_questions} are unrelated to our main topic."
                    if use_chainlit:
                        await cl.Message(content=message).send()
                    logger.warn(message)
