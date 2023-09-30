from typing import List
import chainlit as cl
from asyncer import asyncify
from data_questionnaire_agent.cli.data_questionnaire_agent_cli import (
    process_clarifications,
)

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
    convert_to_question_answers,
)
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice, ResponseQuestions
from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
)
from data_questionnaire_agent.service.question_generation_service import (
    chain_factory_secondary_question,
    prepare_secondary_question,
)
from data_questionnaire_agent.ui.advice_processor import display_advice, process_advice

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
from data_questionnaire_agent.ui.clarifications_chainlit import (
    process_clarifications_chainlit,
)
from data_questionnaire_agent.ui.mail_processor import process_send_email
from data_questionnaire_agent.ui.pdf_processor import generate_display_pdf


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

    advice_sent = await process_questionnaire(settings)
    if not advice_sent:
        await cl.Message(content="Session ended. Please restart the chat by pressing the 'New Chat' button.").send()


async def process_questionnaire(settings: cl.ChatSettings) -> bool:
    minimum_number_of_questions: int = int(settings[MINIMUM_NUMBER_OF_QUESTIONS])
    question_per_batch: int = int(settings[QUESTION_PER_BATCH])
    initial_question: str = settings[INITIAL_QUESTION]

    await setup_avatar()

    questions: List[QuestionAnswer] = [
        QuestionAnswer.question_factory(initial_question)
    ]
    questionnaire = Questionnaire([])

    await loop_questions(questions, questionnaire)

    generated_questions = await process_initial_question(questionnaire, question_per_batch)
    await loop_questions(generated_questions, questionnaire)

    has_advice = False
    while len(questionnaire) <= minimum_number_of_questions or not has_advice:
        generated_questions = await process_secondary_questions(questionnaire, question_per_batch)
        await loop_questions(generated_questions, questionnaire)
        if len(questionnaire) > minimum_number_of_questions:
            conditional_advice: ConditionalAdvice = await process_advice(docsearch, questionnaire)
            has_advice = conditional_advice.has_advice
            if has_advice:
                await display_advice(conditional_advice)
                await generate_display_pdf(conditional_advice, questionnaire)
                await process_send_email(questionnaire, conditional_advice)
                return True
    return False


async def loop_questions(questions: List[QuestionAnswer], questionnaire: Questionnaire):
    for question in questions:
        response = None
        while response is None:
            response = await cl.AskUserMessage(
                content=question.question,
                timeout=cfg.ui_timeout,
                author=AVATAR["CHATBOT"],
            ).send()
        logger.info("",response)
        question.answer = response["content"]
    questionnaire.questions.extend(questions)
    await process_clarifications_chainlit(questionnaire, len(questions))


async def process_initial_question(
    questionnaire: Questionnaire, question_per_batch: int
) -> List[QuestionAnswer]:
    question = questionnaire.questions[-1]
    answer = question.answer
    initial_question_chain = await asyncify(chain_factory_initial_question)()
    knowledge_base = await asyncify(similarity_search)(
        docsearch, answer, how_many=cfg.search_results_how_many
    )
    input = prepare_initial_question(
        question=question.question,
        answer=answer,
        questions_per_batch=question_per_batch,
        knowledge_base=knowledge_base,
    )
    response_questions: ResponseQuestions = await initial_question_chain.arun(input)
    return convert_to_question_answers(response_questions)


async def process_secondary_questions(
    questionnaire: Questionnaire, question_per_batch: int
) -> List[QuestionAnswer]:
    knowledge_base = similarity_search(
        docsearch, questionnaire.answers_str(), how_many=cfg.search_results_how_many
    )
    secondary_question_chain = await asyncify(chain_factory_secondary_question)()
    secondary_question_input = prepare_secondary_question(
        questionnaire, knowledge_base, question_per_batch
    )
    response_questions: ResponseQuestions = await secondary_question_chain.arun(
        secondary_question_input
    )
    return convert_to_question_answers(response_questions)
