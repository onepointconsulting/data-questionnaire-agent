from typing import List, Any, Tuple, Union
from enum import StrEnum

import socketio
import json
from aiohttp import web
from asyncer import asyncify

from langchain_community.callbacks import get_openai_callback

from data_questionnaire_agent.config import websocket_cfg, mail_config
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.server.agent_session import AgentSession, agent_sessions
from data_questionnaire_agent.model.server_model import (
    ServerMessage,
    ServerMessages,
    server_messages_factory,
)
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.session_configuration import (
    SessionConfigurationEntry,
    SESSION_STEPS_CONFIG_KEY,
    DEFAULT_SESSION_STEPS,
    SessionConfiguration,
)
from data_questionnaire_agent.model.mail_data import MailData
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.service.persistence_service_async import (
    insert_questionnaire_status,
    select_questionnaire,
    select_initial_question,
    select_suggestions,
    update_answer,
    select_questionnaire,
    select_questionnaire_statuses,
    select_report,
    save_session_configuration,
    select_session_configuration,
    select_current_session_steps,
    save_report,
    insert_questionnaire_status_suggestions,
    select_questionnaire_status_suggestions,
    update_session_steps,
)
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
)
from data_questionnaire_agent.service.secondary_question_processor import (
    process_secondary_questions,
)
from data_questionnaire_agent.ui.advice_processor import process_advice
from data_questionnaire_agent.service.advice_service import chain_factory_advice
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.html_generator import generate_pdf_from
from data_questionnaire_agent.service.mail_sender import send_email
from data_questionnaire_agent.service.mail_sender import create_mail_body
from data_questionnaire_agent.service.question_clarifications import (
    chain_factory_question_clarifications,
)


CORS_HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"}
FAILED_SESSION_STEPS = -1
MAX_SESSION_STEPS = 14

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
    CLARIFICATION_TOKEN = "clarification_token"
    EXTEND_SESSION = "extend_session"
    ERROR = "error"


@sio.event
async def connect(sid: str, environ):
    logger.info(f"connect {sid}")


@sio.event
def disconnect(sid):
    logger.info(f"disconnect {sid}")


@sio.event
async def start_session(sid: str, client_session: str, session_steps: int = 6):
    """
    Start the session by setting the main topic.
    """
    agent_session = AgentSession(sid, client_session)
    session_id = agent_session.session_id
    questionnaire_messages = await select_questionnaire_statuses(session_id)
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

    await append_first_suggestion(server_messages, question)
    await append_other_suggestions(server_messages, questionnaire_messages)
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
        questionnaire = await select_questionnaire(session_id)
        current_session_steps = await select_current_session_steps(session_id)
        if current_session_steps - 1 > len(questionnaire):
            await handle_secondary_question(sid, session_id, questionnaire)
        else:
            # Check if report is available
            report = await select_report(session_id)

            if report is None:
                # Generate the report.
                await generate_report(session_id, questionnaire)

            questionnaire_messages = await select_questionnaire_statuses(session_id)
            server_messages = server_messages_factory(questionnaire_messages)
            await append_suggestions_and_send(
                sid, server_messages, questionnaire_messages
            )


@sio.event
async def clarify_question(sid: str, session_id: str, question: str):
    async for token in await chain_factory_question_clarifications(question):
        content = token.content
        await sio.emit(
            Commands.CLARIFICATION_TOKEN,
            content,
            room=sid,
        )


@sio.event
async def extend_session(sid: str, session_id: str, session_steps: int):
    session_steps = min(MAX_SESSION_STEPS, session_steps)
    config_id = await update_session_steps(session_id, session_steps)
    session_steps = session_steps if config_id is not None else FAILED_SESSION_STEPS
    await sio.emit(
        Commands.EXTEND_SESSION,
        session_steps,
        room=sid,
    )


async def generate_report(session_id: str, questionnaire: Questionnaire):
    total_cost = 0
    with get_openai_callback() as cb:
        conditional_advice: ConditionalAdvice = await process_advice(
            docsearch, questionnaire, advice_chain
        )
        total_cost = cb.total_cost
    report_id = await save_report(session_id, conditional_advice, total_cost)
    assert report_id is not None, "Report ID is not available."


async def handle_secondary_question(
    sid: str, session_id: str, questionnaire: Questionnaire
):
    total_cost = 0
    with get_openai_callback() as cb:
        question_answers = await process_secondary_questions(
            questionnaire, cfg.questions_per_batch
        )
        total_cost = cb.total_cost
    if len(question_answers) == 0:
        await send_error(sid, session_id, "Could not get any answers from ChatGPT.")
        return
    last_question_answer = question_answers[-1]
    # Save the generated question
    _, qs_res = await persist_question(
        session_id, last_question_answer.question, total_cost
    )
    # Persist the suggestions for this answer
    if qs_res.id is None:
        await send_error(sid, session_id, "Failed to insert question in database.")
        return
    await insert_questionnaire_status_suggestions(qs_res.id, last_question_answer)
    questionnaire_messages = await select_questionnaire_statuses(session_id)
    server_messages = server_messages_factory(questionnaire_messages)

    await append_suggestions_and_send(sid, server_messages, questionnaire_messages)


async def append_suggestions_and_send(
    sid: str,
    server_messages: ServerMessages,
    questionnaire_messages: List[QuestionnaireStatus],
):
    await append_first_suggestion(server_messages, questionnaire_messages[0].question)
    await append_other_suggestions(server_messages, questionnaire_messages)
    await sio.emit(
        Commands.SERVER_MESSAGE,
        server_messages.json(),
        room=sid,
    )


async def append_other_suggestions(server_messages, questionnaire_messages):
    if len(questionnaire_messages) > 1:
        for i, message in enumerate(questionnaire_messages[1:]):
            server_messages.server_messages[
                i + 1
            ].suggestions = await select_questionnaire_status_suggestions(message.id)


async def persist_question(session_id: str, question: str, total_cost: int = 0):
    qs = QuestionnaireStatus(
        session_id=session_id,
        question=question,
        final_report=False,
        total_cost=total_cost,
    )
    qs_res = await insert_questionnaire_status(qs)
    return qs, qs_res


async def append_first_suggestion(server_messages: ServerMessages, question: str):
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


@routes.get("/pdf/{session_id}")
async def get_pdf(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    questionnaire, advices = await query_questionnaire_advices(session_id)
    logger.info("PDF advices: %s", advices)
    report_path = generate_pdf_from(questionnaire, advices)
    logger.info("PDF report_path: %s", report_path)
    content_disposition = "attachment"
    return web.FileResponse(
        report_path,
        headers={
            "CONTENT-DISPOSITION": f'{content_disposition}; filename="{report_path.name}"'
        },
    )


@routes.options("/email/{session_id}")
async def send_email_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/email/{session_id}")
async def send_email_request(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    questionnaire, advices = await query_questionnaire_advices(session_id)
    if len(questionnaire.questions) == 0:
        return web.Response(
            text=json.dumps({"error": f"Invalid Session: {session_id}"}),
            status=400,
            content_type="application/json",
            headers=CORS_HEADERS,
        )
    try:
        data: Any = await request.json()
        mail_data = MailData.parse_obj(data)
        mail_body = create_mail_body(questionnaire, advices)
        # Respond with a JSON message indicating success
        await asyncify(send_email)(
            mail_data.person_name, mail_data.email, mail_config.mail_subject, mail_body
        )
        return web.json_response(
            {"message": "Mail sent successfully."}, headers=CORS_HEADERS
        )
    except json.JSONDecodeError:
        # In case of a JSON parsing error, return an error response
        return web.Response(
            text=json.dumps({"error": "Invalid JSON"}),
            status=400,
            content_type="application/json",
            headers=CORS_HEADERS,
        )


def extract_session(request):
    session_id = request.match_info.get("session_id", None)
    logger.info("PDF session_id: %s", session_id)
    if session_id is None:
        raise web.HTTPNotFound(text="No session id specified")
    return session_id


async def query_questionnaire_advices(
    session_id: str,
) -> Tuple[Questionnaire, Union[ConditionalAdvice, None]]:
    questionnaire = await select_questionnaire(session_id, False)
    advices = await select_report(session_id)
    return questionnaire, advices