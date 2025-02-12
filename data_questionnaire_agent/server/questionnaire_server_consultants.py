from aiohttp import web

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    extract_language,
    extract_session,
    routes,
)
from data_questionnaire_agent.service.consultant_service import (
    calculate_consultant_ratings_for,
)


@routes.options("/consultant/ratings/{session_id}")
async def consultant_ratings(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.get("/consultant/ratings/{session_id}")
async def consultant_ratings(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    language = extract_language(request)
    consultant_ratings = await calculate_consultant_ratings_for(session_id, language)
    if not consultant_ratings:
        raise web.HTTPBadRequest(
            text="Cannot find any consultant ratings for that report, because either the session does not exist or does not have a final report.",
            headers=CORS_HEADERS,
        )
    logger.info("Generating consultant advice for: %s", session_id)
    return web.json_response(consultant_ratings.dict(), headers=CORS_HEADERS)
