import chainlit as cl
from asyncer import asyncify
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseTags
from data_questionnaire_agent.service.clarifications_agent import create_clarification_agent

from data_questionnaire_agent.service.tagging_service import prepare_sentiment_input, sentiment_chain_factory


async def process_clarifications_chainlit(questionnaire: Questionnaire, questions_to_process: int):
    questions = questionnaire.questions[-questions_to_process:]
    content = "\n".join([q.answer for q in questions])
    has_questions_chain = await asyncify(sentiment_chain_factory)()
    response_tags: ResponseTags = await has_questions_chain.arun(
        prepare_sentiment_input(content)
    )
    if len(response_tags.extracted_questions) > 0:
        clarification_agent = await asyncify(create_clarification_agent)()
        for clarification_question in response_tags.extracted_questions:
            clarification = await clarification_agent.arun(clarification_question)
            await cl.Message(content=clarification).send()

