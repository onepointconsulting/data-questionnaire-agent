import json

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.server.server_support import CORS_HEADERS, handle_error, routes
from aiohttp import web

from data_questionnaire_agent.service.persistence_service_questions_async import select_sessions_completed_data


@routes.options("/session/completed")
async def verify_sessions_completed_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.get("/session/completed")
async def verify_sessions_completed(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        session_ids = extract_sessions(request)
        sessions = await select_sessions_completed_data(session_ids)
        # Use model_dump_json() to properly serialize datetime objects, then parse back to dict
        return web.json_response(json.loads(sessions.model_dump_json()), headers=CORS_HEADERS)
    return await handle_error(process, request=request)


def extract_sessions(request: web.Request) -> list[str]:
    session_ids = request.query.get("session_ids", None)
    if session_ids is None:
        raise web.HTTPNotFound(text="No session ids specified")
    logger.info("Session ids: %s", session_ids)
    return session_ids.split(",")