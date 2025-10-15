import time
import asyncio
import json
import ipaddress
from enum import StrEnum
from typing import Any, List, Tuple, Union
from collections import defaultdict, deque

import socketio
from aiohttp import web
from asyncer import asyncify
from langchain_community.callbacks import get_openai_callback

from data_questionnaire_agent.config import cfg, mail_config, websocket_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.model.jwt_token import JWTTokenData
from data_questionnaire_agent.model.mail_data import MailData
from data_questionnaire_agent.model.openai_schema import (
    ConditionalAdvice,
    ResponseQuestions,
)
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.server_model import (
    ErrorMessage,
    ServerMessage,
    ServerMessages,
    server_messages_factory,
)
from data_questionnaire_agent.model.session_configuration import (
    DEFAULT_SESSION_STEPS,
    SESSION_STEPS_CONFIG_KEY,
    ChatType,
    SessionConfiguration,
    SessionConfigurationEntry,
    SessionProperties,
    chat_type_factory,
    create_session_configurations,
)
from data_questionnaire_agent.server.agent_session import AgentSession, agent_sessions
from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    extract_language,
    extract_session,
    handle_error,
    routes,
)
from data_questionnaire_agent.service.advice_service import (
    create_structured_question_call,
)
from data_questionnaire_agent.service.confidence_service import (
    calculate_confidence_rating,
)
from data_questionnaire_agent.service.graph_service import generate_analyzed_ontology
from data_questionnaire_agent.service.html_generator import generate_pdf_from
from data_questionnaire_agent.service.jwt_token_service import (
    decode_token,
    generate_token,
    generate_token_batch_file,
)
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.service.language_adapter import adapt_language
from data_questionnaire_agent.service.mail_sender import create_mail_body, send_email
from data_questionnaire_agent.service.ontology_service import create_ontology
from data_questionnaire_agent.service.persistence_service_async import (
    delete_last_question,
    fetch_ontology,
    has_final_report,
    insert_questionnaire_status,
    insert_questionnaire_status_suggestions,
    save_confidence,
    save_ontology,
    save_report,
    save_session_configuration,
    select_confidence,
    select_current_session_steps_and_language,
    select_global_configuration,
    select_questionnaire,
    select_questionnaire_status_suggestions,
    select_questionnaire_statuses,
    select_report,
    select_session_configuration,
    update_answer,
    update_clarification,
    update_regenerated_question,
    update_session_steps,
)
from data_questionnaire_agent.service.persistence_service_questions_async import (
    select_initial_question,
    select_outstanding_questions,
    select_suggestions,
)
from data_questionnaire_agent.service.question_clarifications import (
    chain_factory_question_clarifications,
)
from data_questionnaire_agent.service.question_generation_service import (
    create_structured_question_call as create_structured_regeneration_call,
)
from data_questionnaire_agent.service.question_generation_service import (
    prepare_secondary_question,
)
from data_questionnaire_agent.service.report_aggregation_main_service import (
    aggregate_reports_main,
)
from data_questionnaire_agent.service.secondary_question_processor import (
    process_secondary_questions,
)
from data_questionnaire_agent.service.add_more_suggestions_service import (
    process_add_more_suggestions,
)
from data_questionnaire_agent.translation import t
from data_questionnaire_agent.ui.advice_processor import process_advice

FAILED_SESSION_STEPS = -1
MAX_SESSION_STEPS = 14


sio = socketio.AsyncServer(
    cors_allowed_origins=websocket_cfg.websocket_cors_allowed_origins,
    ping_timeout=10,
    ping_interval=15,
    max_http_buffer_size=1_000_000,
)


@web.middleware
async def rate_limit(request, handler):
    # Only apply rate limiting to socket.io requests
    if not request.path.startswith("/socket.io/"):
        return await handler(request)
    
    ip = extract_client_ip(request)
    now = time.monotonic()
    q = hits[ip]
    
    # Clean old timestamps
    while q and now - q[0] > WINDOW:
        q.popleft()
    
    # Check rate limit
    if len(q) >= MAX_REQ:
        return web.Response(status=429, text="Too Many Requests")
    
    # Add current request timestamp
    q.append(now)
    return await handler(request)


app = web.Application(middlewares=[rate_limit])
sio.attach(app)


@web.middleware
async def startup_cleanup_task(request, handler):
    """Start the cleanup task on first request if not already started."""
    if not hasattr(startup_cleanup_task, 'cleanup_started'):
        asyncio.create_task(cleanup_inactive_ips())
        startup_cleanup_task.cleanup_started = True
        logger.info("Started IP cleanup background task")
    return await handler(request)


# Add startup middleware to begin cleanup task
app.middlewares.append(startup_cleanup_task)


class Commands(StrEnum):
    START_SESSION = "start_session"
    SERVER_MESSAGE = "server_message"
    CLARIFICATION_TOKEN = "clarification_token"
    EXTEND_SESSION = "extend_session"
    ERROR = "error"
    REGENERATE_QUESTION = "regenerate_question"
    ADD_MORE_SUGGESTIONS = "add_more_suggestions"


WINDOW, MAX_REQ = 1.0, 10  # 10 req/sec per IP
CLEANUP_INTERVAL = 300  # Clean up every 5 minutes
hits = defaultdict(deque)


def extract_client_ip(request) -> str:
    """Extract and validate client IP address from request headers."""
    # Check X-Forwarded-For header (for reverse proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        client_ip = forwarded_for.split(",")[0].strip()
        try:
            # Validate IP address
            ipaddress.ip_address(client_ip)
            return client_ip
        except ValueError:
            pass
    
    # Fall back to direct connection IP
    if request.remote:
        try:
            ipaddress.ip_address(request.remote)
            return request.remote
        except ValueError:
            pass
    
    # If all else fails, return a default identifier
    return "unknown"


async def cleanup_inactive_ips():
    """Periodically clean up inactive IP addresses to prevent memory leaks."""
    while True:
        try:
            await asyncio.sleep(CLEANUP_INTERVAL)
            now = time.monotonic()
            inactive_ips = []
            
            for ip, timestamps in hits.items():
                # Remove old timestamps
                while timestamps and now - timestamps[0] > WINDOW:
                    timestamps.popleft()
                
                # If no recent activity, mark for removal
                if not timestamps:
                    inactive_ips.append(ip)
            
            # Remove inactive IPs
            for ip in inactive_ips:
                del hits[ip]
                
            if inactive_ips:
                logger.info(f"Cleaned up {len(inactive_ips)} inactive IP addresses")
                
        except Exception as e:
            logger.error(f"Error during IP cleanup: {e}")


@sio.event
async def connect(sid: str, environ):
    logger.info(f"connect {sid}")


@sio.event
def disconnect(sid: str):
    logger.info(f"disconnect {sid}")


@sio.event
async def start_session(
    sid: str,
    client_session: str,
    session_steps: int = 6,
    language: str = "en",
    client_id: str = "",
    chat_type: str = ChatType.DIVERGING.value,
):
    """
    Start the session by setting the main topic.
    """
    language = adapt_language(language)
    agent_session = AgentSession(sid, client_session)
    session_id = agent_session.session_id
    questionnaire_messages = await select_questionnaire_statuses(session_id)
    server_messages = None
    question = None

    global_configuration = await select_global_configuration()
    if len(questionnaire_messages) == 0:
        # No question yet. Start from scratch
        id, question = await select_initial_question(language)
        qs, qs_res = await persist_question(session_id, question, id)
        if qs_res is None or qs_res.id is None:
            await send_error(sid, session_id, t("db_insert_failed", locale=language))
            return
        server_messages = server_messages_factory([qs])
        session_properties = SessionProperties(
            session_steps=global_configuration.get_default_session_steps(
                DEFAULT_SESSION_STEPS
            )
            or session_steps,
            session_language=language,
            chat_type=chat_type_factory(chat_type),
        )
        await insert_configuration(server_messages, session_properties, client_id)
    else:
        # Get all messages on this session
        server_messages = server_messages_factory(questionnaire_messages)
        question = questionnaire_messages[0].question
        await load_configuration(server_messages)
    server_messages.global_configuration = global_configuration

    await append_first_suggestion(server_messages, question)
    await append_other_suggestions(server_messages, questionnaire_messages)
    await sio.emit(
        Commands.START_SESSION,
        server_messages.json(),
        room=sid,
    )


@sio.event
async def client_message(sid: str, session_id: str, answer: str):
    if session_id not in agent_sessions:
        await handle_missing_session(sid, session_id)
    else:
        update_id = await update_answer(session_id, answer)
        session_properties: SessionProperties = (
            await select_current_session_steps_and_language(session_id)
        )
        language = session_properties.session_language
        current_session_steps = session_properties.session_steps
        if update_id is None:
            await send_error(sid, session_id, t("db_update_failed", locale=language))
            return
        questionnaire = await select_questionnaire(session_id)
        if current_session_steps > len(questionnaire):
            # We are generating questions
            await handle_secondary_question(
                sid, session_id, questionnaire, session_properties
            )
        else:
            # Check if report is available
            report = await select_report(session_id)

            if report is None:
                # Generate the report.
                await generate_report(session_id, questionnaire, language)

            await send_report_message(sid, session_id)


@sio.event
async def regenerate_question(sid: str, session_id: str):
    if session_id not in agent_sessions:
        await handle_missing_session(sid, session_id)
    else:
        try:
            session_properties: SessionProperties = (
                await select_current_session_steps_and_language(session_id)
            )
            runnable = create_structured_regeneration_call(
                session_properties, is_recreate=True
            )
            questionnaire = await select_questionnaire(session_id)
            knowledge_base = await fetch_context(questionnaire)
            confidence_rating = await calculate_confidence_rating(
                questionnaire, session_properties.session_language
            )
            input = prepare_secondary_question(
                questionnaire,
                knowledge_base,
                questions_per_batch=1,
                is_recreate=True,
                confidence_rating=confidence_rating,
            )
            res: ResponseQuestions = await runnable.ainvoke(input)
            # replace latest question in the database.
            previous_question = questionnaire.questions[-1]
            new_question = res.questions[-1]
            # replace suggestions too
            suggestions = res.possible_answers
            await update_regenerated_question(
                session_id, previous_question.question, new_question, suggestions
            )
            await select_all_messages_and_send(sid, session_id, is_regenerate=True)
        except Exception as e:
            logger.error(str(e))
            await sio.emit(
                Commands.REGENERATE_QUESTION,
                ErrorMessage(
                    session_id=session_id,
                    error=t(
                        "regeneration_failed",
                        locale=session_properties.session_language,
                    ),
                ).json(),
                room=sid,
            )


async def handle_missing_session(sid: str, session_id: str):
    logger.warning(f"Session not found {session_id}")
    # Create new session
    await start_session(sid, session_id)


async def send_report_message(sid: str, session_id: str):
    questionnaire_messages = await select_questionnaire_statuses(session_id)
    server_messages = server_messages_factory(questionnaire_messages)
    await append_suggestions_and_send(sid, server_messages, questionnaire_messages)


@sio.event
async def generate_report_now(sid: str, session_id: str):
    questionnaire = await select_questionnaire(session_id)
    new_session_steps = len(questionnaire.questions)
    config_id = await update_session_steps(session_id, new_session_steps)
    session_properties = await select_current_session_steps_and_language(session_id)
    language = session_properties.session_language
    current_session_steps = session_properties.session_steps
    if config_id is None or current_session_steps != new_session_steps:
        await send_error(sid, session_id, "Failed to generate report now")
    else:
        delete_id = await delete_last_question(session_id)
        if delete_id is None:
            logger.warn("Could not delete last question in generate report now.")
        await generate_report(session_id, questionnaire, language)
        await send_report_message(sid, session_id)


@sio.event
async def clarify_question(
    sid: str, session_id: str, question: str, language: str = "en"
):
    language = adapt_language(language)
    clarification = ""
    async for token in await chain_factory_question_clarifications(question, language):
        content = token.content
        clarification += content
        await sio.emit(
            Commands.CLARIFICATION_TOKEN,
            content,
            room=sid,
        )
    await update_clarification(session_id, question, clarification)


@sio.event
async def add_more_suggestions(
    sid: str, session_id: str, question: str, language: str = "en"
):
    language = adapt_language(language)
    try:
        possible_answers = await process_add_more_suggestions(
            session_id, question, language
        )
        await sio.emit(
            Commands.ADD_MORE_SUGGESTIONS,
            possible_answers.json(),
            room=sid,
        )
    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        await sio.emit(
            Commands.ADD_MORE_SUGGESTIONS,
            ErrorMessage(
                session_id=session_id,
                error=t("add_more_suggestions_failed", locale=language) + f" {error_message}",
            ).json(),
            room=sid,
        )


@sio.event
async def extend_session(sid: str, session_id: str, session_steps: int):
    final_report = await has_final_report(session_id)
    if final_report:
        session_properties = await select_current_session_steps_and_language(session_id)
        await sio.emit(
            Commands.EXTEND_SESSION,
            session_properties.session_steps,
            room=sid,
        )
        return
    session_steps = min(MAX_SESSION_STEPS, session_steps)
    config_id = await update_session_steps(session_id, session_steps)
    session_steps = session_steps if config_id is not None else FAILED_SESSION_STEPS
    await sio.emit(
        Commands.EXTEND_SESSION,
        session_steps,
        room=sid,
    )


async def generate_report(session_id: str, questionnaire: Questionnaire, language: str):
    language = adapt_language(language)
    total_cost = 0
    with get_openai_callback() as cb:
        confidence_rating = await find_confidence_rating(
            session_id, len(questionnaire) - 1, questionnaire, language
        )
        conditional_advice = await process_advice(
            questionnaire, create_structured_question_call(language)
        )
        await save_confidence_rating(
            confidence_rating, conditional_advice, session_id, questionnaire
        )
        total_cost = cb.total_cost
        # Generate ontology
        ontology = await create_ontology(questionnaire, conditional_advice, language)
        ontology = generate_analyzed_ontology(ontology)
        await save_ontology(session_id, ontology)
    report_id = await save_report(session_id, conditional_advice, total_cost)
    assert report_id is not None, t("no_report_id", locale=language)


async def handle_secondary_question(
    sid: str,
    session_id: str,
    questionnaire: Questionnaire,
    session_properties: SessionProperties,
):
    language = session_properties.session_language
    total_cost = 0
    # Find outstanding questions
    question_answers = await select_outstanding_questions(language, session_id)
    if len(question_answers) == 0:
        # Generate questions using AI
        with get_openai_callback() as cb:
            confidence_rating = await calculate_confidence_rating(
                questionnaire, language
            )
            question_answers = (
                await process_secondary_questions(
                    questionnaire,
                    cfg.questions_per_batch,
                    session_properties,
                    session_id,
                    confidence_rating,
                ),
            )
            total_cost = cb.total_cost
    else:
        confidence_rating = await calculate_confidence_rating(questionnaire, language)
    if len(question_answers) == 0:
        await send_error(sid, session_id, t("no_answer_from_chatgpt", locale=language))
        return
    last_question_answer = question_answers[0][0]
    # Save the generated question
    _, qs_res = await persist_question(
        session_id, last_question_answer.question, last_question_answer.id, total_cost
    )
    await save_confidence_rating(confidence_rating, None, session_id, questionnaire)
    # Persist the suggestions for this answer
    if qs_res.id is None:
        await send_error(sid, session_id, t("failed_insert_question", locale=language))
        return
    await insert_questionnaire_status_suggestions(qs_res.id, last_question_answer)
    await select_all_messages_and_send(sid, session_id)


async def select_all_messages_and_send(
    sid: str, session_id: str, is_regenerate: bool = False
):
    questionnaire_messages = await select_questionnaire_statuses(session_id)
    server_messages = server_messages_factory(questionnaire_messages)

    await append_suggestions_and_send(
        sid, server_messages, questionnaire_messages, is_regenerate
    )


async def save_confidence_rating(
    confidence_rating: Union[ConfidenceRating, None],
    conditional_advice: Union[ConditionalAdvice, None],
    session_id: str,
    questionnaire: Questionnaire,
):
    if confidence_rating is not None:
        step = len(questionnaire.questions)

        # Prevent the confidence rating from decreasing
        previous_confidence_rating = None
        if step is not None and step > 2:
            previous_confidence_rating = await select_confidence(session_id, step - 1)
            if (
                previous_confidence_rating is not None
                and previous_confidence_rating is not None
            ):
                if previous_confidence_rating > confidence_rating:
                    confidence_rating = previous_confidence_rating

        # Save the confidence
        if conditional_advice:
            conditional_advice.confidence = confidence_rating
        await save_confidence(session_id, step, confidence_rating)


async def append_suggestions_and_send(
    sid: str,
    server_messages: ServerMessages,
    questionnaire_messages: List[QuestionnaireStatus],
    is_regenerate: bool = False,
):
    await append_first_suggestion(server_messages, questionnaire_messages[0].question)
    await append_other_suggestions(server_messages, questionnaire_messages)
    await sio.emit(
        Commands.SERVER_MESSAGE if not is_regenerate else Commands.REGENERATE_QUESTION,
        server_messages.json(),
        room=sid,
    )


async def append_other_suggestions(server_messages, questionnaire_messages):
    if len(questionnaire_messages) > 1:
        for i, message in enumerate(questionnaire_messages[1:]):
            server_messages.server_messages[
                i + 1
            ].suggestions = await select_questionnaire_status_suggestions(message.id)


async def persist_question(
    session_id: str, question: str, question_id: int | None, total_cost: int = 0
):
    qs = QuestionnaireStatus(
        session_id=session_id,
        question=question,
        final_report=False,
        total_cost=total_cost,
        question_id=question_id,
    )
    qs_res = await insert_questionnaire_status(qs)
    return qs, qs_res


async def append_first_suggestion(server_messages: ServerMessages, question: str):
    server_messages.server_messages[0].suggestions = await select_suggestions(question)


async def insert_configuration(
    server_messages: ServerMessages,
    session_properties: SessionProperties,
    client_id: str = "",
):
    session_id = server_messages.session_id
    session_keys = create_session_configurations(
        session_id=session_id,
        session_properties=session_properties,
        client_id=client_id,
    )
    accepted_keys = []
    for session_key in session_keys:
        saved_entry = await save_session_configuration(session_key)
        if saved_entry is None:
            # Something went wrong. We will use the default value.
            logger.error(
                f"Could not save configuration with {session_key.config_key}: {session_key.config_value}"
            )
        else:
            accepted_keys.append(session_key)
    session_configuration = SessionConfiguration(configuration_entries=accepted_keys)
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
            question=error_message,
            session_id=session_id,
            clarification="",
            suggestions=[],
            question_id=None,
        ).json(),
        room=sid,
    )


@routes.get("/pdf/{session_id}")
async def get_pdf(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    questionnaire, advices = await query_questionnaire_advices(session_id)
    logger.info("PDF advices: %s", advices)
    language = extract_language(request)
    report_path = generate_pdf_from(questionnaire, advices, language)
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
        language = extract_language(request)
        data: Any = await request.json()
        mail_data = MailData.parse_obj(data)
        mail_body = create_mail_body(questionnaire, advices, language=language)
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


@routes.get("/ontology/{session_id}")
async def ontology(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    relationships = await fetch_ontology(session_id)
    return web.json_response(relationships, headers=CORS_HEADERS)


@routes.get("/confidence/{session_id}")
async def confidence(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    step = extract_step(request)
    questionnaire = await select_questionnaire(session_id, False)
    language = extract_language(request)
    confidence_rating = await find_confidence_rating(
        session_id, step, questionnaire, language
    )
    if confidence_rating is None:
        raise web.HTTPInternalServerError(text="No confidence rating could be found.")
    else:
        logger.info(f"confidence available {confidence_rating}")
    return web.json_response(confidence_rating.dict(), headers=CORS_HEADERS)


@routes.options("/gen_jwt_token")
async def generate_jwt_token_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/gen_jwt_token")
async def generate_jwt_token(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"name": name, "email": email}:
                time_delta_minutes = extract_time_delta(json_content)
                token = await generate_token(
                    JWTTokenData(
                        name=name, email=email, time_delta_minutes=time_delta_minutes
                    )
                )
                return web.json_response(token.dict(), headers=CORS_HEADERS)
            case _:
                raise web.HTTPBadRequest(
                    text="Please provide name and email parameters in the JSON body",
                    headers=CORS_HEADERS,
                )

    return await handle_error(process, request=request)


@routes.options("/generate_token_batch")
async def generate_token_batch_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/generate_token_batch")
async def generate_token_batch_post(request: web.Request) -> web.Response:
    """
    Generates a batch of tokens
    Example:
    {
        "name": "anonymous_postman",
        "email": "anonymous_postman@test.com",
        "time_delta_minutes": 60,
        "amount": 3
    }
    """

    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"name": name, "email": email, "amount": amount}:
                time_delta_minutes = extract_time_delta(json_content)
                token_data = JWTTokenData(
                    name=name, email=email, time_delta_minutes=time_delta_minutes
                )
                generated = await generate_token_batch_file(token_data, amount)
                content_disposition = "attachment"
                return web.FileResponse(
                    generated,
                    headers={
                        **CORS_HEADERS,
                        "CONTENT-DISPOSITION": f'{content_disposition}; filename="{generated.name}"',
                    },
                )
            case _:
                raise web.HTTPBadRequest(
                    text="Please provide name, email and time_delta_minutes parameters in the JSON body",
                    headers=CORS_HEADERS,
                )

    return await handle_error(process, request=request)


@routes.post("/validate_jwt_token")
async def validate_jwt_token(request: web.Request) -> web.Response:
    try:
        json_content = await request.json()
        match json_content:
            case {"token": token}:
                try:
                    decoded = await decode_token(token)
                except Exception:
                    raise web.HTTPBadRequest(
                        text="The token does not seem to be valid. Please send another valid token.",
                        headers=CORS_HEADERS,
                    )
                return web.json_response(decoded, headers=CORS_HEADERS)
            case _:
                raise web.HTTPBadRequest(
                    text="Please provide the token in the JSON body",
                    headers=CORS_HEADERS,
                )
    except json.JSONDecodeError as e:
        raise web.HTTPBadRequest(
            text=f"Please make sure the JSON body is available and well formatted: {e}"
        )


@routes.options("/generate_aggregated_report")
async def generate_aggregated_report_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/generate_aggregated_report")
async def generate_aggregated_report(request: web.Request) -> web.Response:
    """
    Example:
    {
        "tokens": [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEMkpXTkhBNTZGN1lHRENDU1czRjJaQiIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MzIwMzI0ODR9.r8LTAiuORLPk2QnrS8YMcX7dHdlYKndHuXc3PEY6Msw",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEVDY0S1gxR0hTSktTQVcwSE1aSEhERyIsIm5hbWUiOiJUZXN0XzQiLCJpYXQiOjE3MzI4MjQ0MjB9.PUMd-BBH3SjuXdlG8SWQXsvCJApRW7xy_giEVx84yA4"
        ],
        "language": "de",
        "email_list": "gil.fernandes@gmail.com"
    }
    """

    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"tokens": tokens, "language": language}:
                email_list = json_content.get("email_list", [])
                if isinstance(email_list, str):
                    email_list = [email_list]
                asyncio.create_task(
                    aggregate_reports_main(tokens, email_list, language)
                )
                return web.json_response(
                    {"result": "OK", "message": "Report submitted successfully."},
                    headers=CORS_HEADERS,
                )
            case _:
                raise web.HTTPBadRequest(
                    text="Please provide the token in the JSON body",
                    headers=CORS_HEADERS,
                )

    return await handle_error(process, request=request)


def extract_time_delta(json_content: dict) -> Union[int, None]:
    return (
        int(json_content["time_delta_minutes"])
        if "time_delta_minutes" in json_content is not None
        else None
    )


async def find_confidence_rating(
    session_id: str, step: int, questionnaire: Questionnaire, language: str
) -> Union[ConfidenceRating, None]:
    confidence_rating = await select_confidence(session_id, step)
    if confidence_rating is not None:
        return confidence_rating
    confidence_rating = await calculate_confidence_rating(questionnaire, language)
    if step is not None and step > 0:
        saved_confidence = await save_confidence(session_id, step, confidence_rating)
        logger.info(f"Saved confidence {saved_confidence}")
    return confidence_rating


def extract_step(request: web.Request) -> int:
    unknown_step = "-1"
    step_str = request.rel_url.query.get("step", unknown_step)
    try:
        return int(step_str)
    except ValueError as _:
        return int(unknown_step)


async def query_questionnaire_advices(
    session_id: str,
) -> Tuple[Questionnaire, Union[ConditionalAdvice, None]]:
    questionnaire = await select_questionnaire(session_id, False)
    advices = await select_report(session_id)
    return questionnaire, advices
