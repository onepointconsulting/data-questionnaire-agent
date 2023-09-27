from typing import List
import chainlit as cl
from asyncer import asyncify
from data_questionnaire_agent.cli.data_questionnaire_agent_cli import process_clarifications

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
)

from data_questionnaire_agent.ui.chat_settings_factory import (
    INITIAL_QUESTION,
    MINIMUM_NUMBER_OF_QUESTIONS,
    QUESTION_PER_BATCH,
    create_chat_settings,
)
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.ui.avatar_factory import AVATAR, setup_avatar

from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
    similarity_search,
)
from data_questionnaire_agent.ui.clarifications_chainlit import process_clarifications_chainlit


docsearch = init_vector_search()


@cl.on_chat_start
async def init():
    """
    Main entry point for the application.
    This application will ask you questions about your data integration strategy and at the end give you some evaluation.
    """
    settings = await create_chat_settings()
    await setup_agent(settings)


@cl.on_settings_update
async def setup_agent(settings: cl.ChatSettings):
    logger.info("Settings: %s", settings)

    await process_questionnaire(settings)


async def process_questionnaire(settings: cl.ChatSettings):
    minimum_number_of_questions: int = int(settings[MINIMUM_NUMBER_OF_QUESTIONS])
    question_per_batch: int = int(settings[QUESTION_PER_BATCH])
    initial_question: str = settings[INITIAL_QUESTION]

    await setup_avatar()

    questions: List[QuestionAnswer] = [
        QuestionAnswer.question_factory(initial_question)
    ]
    questionnaire = Questionnaire([])

    await loop_questions(questions, questionnaire)
    await process_clarifications_chainlit(questionnaire, len(questions))

    generated_questions = await process_initial_question(questionnaire)
    await loop_questions(generated_questions, questionnaire)




async def loop_questions(questions: List[QuestionAnswer], questionnaire: Questionnaire):
    for question in questions:
        response = await cl.AskUserMessage(
            content=question.question,
            timeout=cfg.ui_timeout,
            author=AVATAR["CHATBOT"],
        ).send()
        logger.info(response)
        question.answer = response["content"]
    questionnaire.questions.extend(questions)


async def process_initial_question(questionnaire: Questionnaire) -> List[QuestionAnswer]:
    question = questionnaire.questions[-1]
    answer = question.answer
    initial_question_chain = await asyncify(chain_factory_initial_question)()
    knowledge_base = await asyncify(similarity_search)(docsearch, answer, how_many=cfg.search_results_how_many)
    input = prepare_initial_question(
        question=question.question,
        answer=answer,
        questions_per_batch=cfg.questions_per_batch,
        knowledge_base=knowledge_base,
    )
    response_questions: ResponseQuestions = await initial_question_chain.arun(input)
    generated_questions = [QuestionAnswer.question_factory(q) for q in response_questions.questions]
    return generated_questions


async def process_secondary_questions(questionnaire: Questionnaire, questions_to_process: int) -> List[QuestionAnswer]:
    questions = questionnaire.questions[-questions_to_process:]
