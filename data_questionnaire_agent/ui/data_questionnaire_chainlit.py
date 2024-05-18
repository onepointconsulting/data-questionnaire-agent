########################################
############## Deprecated ##############
########################################

from typing import List
import chainlit as cl
from enum import Enum
from asyncer import asyncify

from tenacity import AsyncRetrying

from data_questionnaire_agent.service.clarifications_agent import (
    create_clarification_agent,
)
from data_questionnaire_agent.service.tagging_service import sentiment_chain_factory
from data_questionnaire_agent.ui.model.session_number_container import (
    SessionNumberContainer,
)

from langchain_community.callbacks import get_openai_callback
from langchain.callbacks.openai_info import OpenAICallbackHandler

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
    convert_to_question_answers,
)
from data_questionnaire_agent.model.initial_question_data import special_question_data
from data_questionnaire_agent.model.openai_schema import (
    ConditionalAdvice,
    ResponseQuestions,
)
from data_questionnaire_agent.service.advice_service import chain_factory_advice
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
from data_questionnaire_agent.toml_support import prompts


class APP_STATE(Enum):
    PROCESSED = 1
    RESTARTED = 2
    EMPTY_ADVICE = 3


@cl.cache
def instantiate_doc_search():
    return init_vector_search()


@cl.cache
def instantiate_initial_question_chain():
    return chain_factory_initial_question()


@cl.cache
def instantiate_secondary_question_chain():
    return chain_factory_secondary_question()


@cl.cache
def instantiate_advice_chain():
    return chain_factory_advice()


@cl.cache
def instantiate_sentiment_chain():
    return sentiment_chain_factory()


@cl.cache
def instantiate_clarification_agent():
    return create_clarification_agent()


docsearch = instantiate_doc_search()

initial_question_chain = instantiate_initial_question_chain()

secondary_question_chain = instantiate_secondary_question_chain()

advice_chain = instantiate_advice_chain()

has_questions_chain = instantiate_sentiment_chain()

clarification_agent = instantiate_clarification_agent()


async def initial_message():
    initial_message = f"""
### Hello! I will ask you a few questions (around {cfg.minimum_questionnaire_size}) about your data ecosystem. At the end, you will get recommendations and suggested courses of action.

- Onepoint’s Data & Analytics Body of Knowledge is the basis for the diagnostics and recommendations.
- If you’d like, you can ask for a copy of the results to be emailed to you.
- This is an experimental tool. Any feedback and improvement ideas are always welcome — thank you!
Let’s get started.

"""
    await cl.Message(content=initial_message, author=AVATAR["CHATBOT"]).send()


@cl.on_chat_start
async def init():
    """
    Main entry point for the application.
    This application will ask you questions about your data integration strategy and at the end give you some evaluation.
    """
    cl.user_session.set("session_counter", SessionNumberContainer())
    await initial_message()
    settings = await create_chat_settings()
    await run_agent(settings)


async def run_agent(settings: cl.ChatSettings):
    """
    Asks questions and anawers questios until it gives advice if the user does not give up.

    Parameters:
    settings cl.ChatSettings: The document list with one page per document.
    """
    logger.info("Settings: %s", settings)

    with get_openai_callback() as cb:
        advice_sent = await process_questionnaire(settings, cb)
        if advice_sent == APP_STATE.EMPTY_ADVICE:
            await cl.Message(
                content=f"Session ended. Please restart the chat by pressing the 'New Chat' button."
            ).send()


@cl.on_settings_update
async def setup_agent(settings: cl.ChatSettings):
    await run_agent(settings)


async def process_questionnaire(
    settings: cl.ChatSettings, cb: OpenAICallbackHandler
) -> APP_STATE:
    minimum_number_of_questions: int = int(settings[MINIMUM_NUMBER_OF_QUESTIONS])
    question_per_batch: int = int(settings[QUESTION_PER_BATCH])
    initial_question: str = settings[INITIAL_QUESTION]

    current_counter = cl.user_session.get("session_counter").increment_and_get()

    await setup_avatar()

    questions: List[QuestionAnswer] = [
        QuestionAnswer.question_factory(initial_question)
    ]
    questionnaire = Questionnaire([])

    looped = await loop_questions(questions, questionnaire, current_counter)
    if not looped:
        return APP_STATE.RESTARTED

    generated_questions = await process_initial_question(
        questionnaire, question_per_batch
    )
    logger.info(f"process_initial_question cost: {cb.total_cost}")
    looped = await loop_questions(generated_questions, questionnaire, current_counter)
    if not looped:
        return APP_STATE.RESTARTED

    has_advice = False
    while len(questionnaire) <= minimum_number_of_questions or not has_advice:
        generated_questions = await process_secondary_questions(
            questionnaire, question_per_batch
        )
        logger.info(f"process_secondary_questions cost: {cb.total_cost}")
        looped = await loop_questions(
            generated_questions, questionnaire, current_counter
        )
        if not looped:
            return APP_STATE.RESTARTED
        if len(questionnaire) > minimum_number_of_questions:
            conditional_advice: ConditionalAdvice = await process_advice(
                docsearch, questionnaire, advice_chain
            )
            logger.info(f"process_advice cost: {cb.total_cost}")
            has_advice = conditional_advice.has_advice
            if has_advice:
                await display_advice(conditional_advice)
                await session_cost(cb)
                await generate_display_pdf(conditional_advice, questionnaire)
                await process_send_email(questionnaire, conditional_advice)
                return APP_STATE.PROCESSED
    return APP_STATE.EMPTY_ADVICE


def process_special_question(question: str) -> str:
    original_question = prompts["questionnaire"]["initial"]["question"]

    def display_options():
        it = iter(special_question_data)
        items = zip(it, it)
        res = ""
        for r1, r2 in items:
            res += f"""
<div class="row init-options-row">
    <div class="col-3 col-md-1 img-cell"><img src="/assets/onepoint/{r1['img_src']}" alt="{r1['img_alt']}" title="{r1['img_alt']}" /></div>
    <div class="col-9 col-md-5"><b>{r1['title']}</b> - {r1['text']}</div>
    <div class="col-3 col-md-1 img-cell"><img src="/assets/onepoint/{r2['img_src']}" alt="{r2['img_alt']}" title="{r2['img_alt']}" /></div>
    <div class="col-9 col-md-5"><b>{r2['title']}</b> - {r2['text']}</div>
</div>
"""
        return res

    if question == original_question:
        return f"""
### {question}
The table below may help with your response — it captures some of the most common data and analytics challenges our clients face.
{display_options()}
"""
    return question


async def loop_questions(
    questions: List[QuestionAnswer], questionnaire: Questionnaire, current_counter: int
) -> bool:
    for question in questions:
        response = None
        while response is None:
            latest_counter = (
                cl.user_session.get("session_counter").current()
                if cl.user_session.get("session_counter") is not None
                else 0
            )
            if latest_counter != current_counter:
                # This means that the current session needs to be terminated
                logger.warn("%s != %s", type(latest_counter), type(current_counter))
                logger.warn("%s != %s", latest_counter, current_counter)
                return False
            response = await cl.AskUserMessage(
                content=process_special_question(question.question),
                timeout=cfg.ui_timeout,
                author=AVATAR["CHATBOT"],
                disable_human_feedback=True,
            ).send()
        logger.info("", response)
        question.answer = response["content"]
    questionnaire.questions.extend(questions)
    await process_clarifications_chainlit(
        questionnaire, len(questions), has_questions_chain, clarification_agent
    )
    return True


async def process_initial_question(
    questionnaire: Questionnaire, question_per_batch: int
) -> List[QuestionAnswer]:
    question = questionnaire.questions[-1]
    answer = question.answer
    knowledge_base = await asyncify(similarity_search)(
        docsearch, answer, how_many=cfg.search_results_how_many
    )
    input = prepare_initial_question(
        question=question.question,
        answer=answer,
        questions_per_batch=question_per_batch,
        knowledge_base=knowledge_base,
    )

    async for attempt in AsyncRetrying(**cfg.retry_args):
        with attempt:
            response_questions: ResponseQuestions = await initial_question_chain.arun(
                input
            )
            return convert_to_question_answers(response_questions)


async def session_cost(cb: OpenAICallbackHandler):
    cost_message = f"Total session cost: {cb.total_cost:.2f} $"
    logger.warn(cost_message)
    if cfg.show_session_cost:
        await cl.Message(content=cost_message).send()
