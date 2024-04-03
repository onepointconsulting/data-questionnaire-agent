from typing import List
from enum import StrEnum

import socketio
from aiohttp import web

from data_questionnaire_agent.config import websocket_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.server.agent_session import AgentSession, agent_sessions
from data_questionnaire_agent.model.server_model import (
    ServerMessage,
    ServerMessages,
    server_messages_factory
)
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.session_configuration import (
    SessionConfigurationEntry,
    SESSION_STEPS_CONFIG_KEY,
    DEFAULT_SESSION_STEPS,
    SessionConfiguration,
)
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.service.persistence_service_async import (
    insert_questionnaire_status,
    select_questionnaire,
    select_initial_question,
    select_suggestions,
    update_answer,
    select_answers,
    save_session_configuration,
    select_session_configuration,
    select_current_session_steps,
    save_report
)
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
)
from data_questionnaire_agent.ui.data_questionnaire_chainlit import (
    process_secondary_questions,
)
from data_questionnaire_agent.ui.advice_processor import process_advice
from data_questionnaire_agent.service.advice_service import chain_factory_advice
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


docsearch = init_vector_search()

advice_chain = chain_factory_advice()

sio = socketio.AsyncServer(
    cors_allowed_origins=websocket_cfg.websocket_cors_allowed_origins
)
app = web.Application()
sio.attach(app)

routes = web.RouteTableDef()


class Commands(StrEnum):
    START_SESSION = "start_session"
    SERVER_MESSAGE = "server_message"
    ERROR = "error"


@sio.event
async def connect(sid: str, environ):
    logger.info(f"connect {sid}")


@sio.event
def disconnect(sid, environ):
    logger.info(f"disconnect {sid} {environ}")


@sio.event
async def start_session(sid: str, client_session: str, session_steps: int = 6):
    """
    Start the session by setting the main topic.
    """
    agent_session = AgentSession(sid, client_session)
    session_id = agent_session.session_id
    questionnaire_messages = await select_questionnaire(session_id)
    server_messages = None
    question = None

    if len(questionnaire_messages) == 0:
        # No question yet. Start from scratch
        question = await select_initial_question()
        qs, qs_res = await persist_question(session_id, question)
        if qs_res.id is None:
            await send_error(sid, session_id, "Failed to insert question in database.")
            return
        server_messages = server_messages_factory([qs])
        await insert_configuration(server_messages, session_steps)
    else:
        # Get all messages on this session
        server_messages = server_messages_factory(questionnaire_messages)
        question = questionnaire_messages[0].question
        await load_configuration(server_messages)

    await append_suggestions(server_messages, question)
    await sio.emit(
        Commands.START_SESSION,
        server_messages.json(),
        room=sid,
    )


@sio.event
async def client_message(sid: str, session_id: str, answer: str):
    if not session_id in agent_sessions:
        logger.warn(f"Session not found {session_id}")
        # Create new session
        await start_session(sid, session_id)
    else:
        update_id = await update_answer(session_id, answer)
        if update_id is None:
            await send_error(
                sid, session_id, "Failed to update the answer in database."
            )
            return
        questionnaire = await select_answers(session_id)
        current_session_steps = await select_current_session_steps(session_id)
        if current_session_steps - 1 > len(questionnaire):
            await handle_secondary_question(sid, session_id, questionnaire)
        else:
            # Generate the report.
            conditional_advice: ConditionalAdvice = await process_advice(
                docsearch, questionnaire, advice_chain
            )
            report_id = await save_report(session_id, conditional_advice)
            assert report_id is not None, "Report ID is not available."
            questionnaire_messages = await select_questionnaire(session_id)
            server_messages = server_messages_factory(
                questionnaire_messages
            )
            await append_suggestions_and_send(
                sid, server_messages, questionnaire_messages
            )


async def handle_secondary_question(
    sid: str, session_id: str, questionnaire: Questionnaire
):
    question_answer = await process_secondary_questions(
        questionnaire, cfg.questions_per_batch
    )
    if len(question_answer) == 0:
        await send_error(sid, session_id, "Could not get any answers from ChatGPT.")
        return
    last_question_answer = question_answer[-1]
    # Save the generated question
    _, qs_res = await persist_question(session_id, last_question_answer.question)
    if qs_res.id is None:
        await send_error(sid, session_id, "Failed to insert question in database.")
        return
    questionnaire_messages = await select_questionnaire(session_id)
    server_messages = server_messages_factory(questionnaire_messages)

    await append_suggestions_and_send(sid, server_messages, questionnaire_messages)


async def append_suggestions_and_send(
    sid: str,
    server_messages: ServerMessages,
    questionnaire_messages: List[QuestionnaireStatus],
):
    await append_suggestions(server_messages, questionnaire_messages[0].question)
    await sio.emit(
        Commands.SERVER_MESSAGE,
        server_messages.json(),
        room=sid,
    )


async def persist_question(session_id, question):
    qs = QuestionnaireStatus(
        session_id=session_id, question=question, final_report=False
    )
    qs_res = await insert_questionnaire_status(qs)
    return qs, qs_res


async def append_suggestions(server_messages: ServerMessages, question: str):
    server_messages.server_messages[0].suggestions = await select_suggestions(question)


async def insert_configuration(server_messages: ServerMessages, session_steps: int):
    session_id = server_messages.session_id
    session_configuration_entry = SessionConfigurationEntry(
        session_id=session_id,
        config_key=SESSION_STEPS_CONFIG_KEY,
        config_value=str(session_steps),
    )
    saved_entry = await save_session_configuration(session_configuration_entry)
    if saved_entry is None:
        # Something went wrong. We will use the dafault value.
        logger.error(f"Could not save configuration with {session_steps}")
    session_configuration = SessionConfiguration(
        configuration_entries=[session_configuration_entry]
    )
    server_messages.session_configuration = session_configuration


async def load_configuration(server_messages: ServerMessages):
    session_id = server_messages.session_id
    session_configuration = await select_session_configuration(session_id)
    if len(session_configuration.configuration_entries) > 0:
        server_messages.session_configuration = session_configuration
    else:
        # Use default values
        entry = SessionConfigurationEntry(
            session_id=session_id,
            config_key=SESSION_STEPS_CONFIG_KEY,
            config_value=DEFAULT_SESSION_STEPS,
        )
        server_messages.session_configuration = SessionConfiguration(
            configuration_entries=[entry]
        )


async def send_error(sid: str, session_id: str, error_message: str):
    await sio.emit(
        Commands.ERROR,
        ServerMessage(
            response=error_message,
            sessionId=session_id,
            suggestions=[],
        ).json(),
        room=sid,
    )
