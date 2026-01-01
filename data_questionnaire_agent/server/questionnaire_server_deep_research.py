from aiohttp import web

from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    extract_language,
    extract_session,
    routes,
)

@routes.options("/deep_research/output/{session_id}")
async def deep_research_output_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.get("/deep_research/output/{session_id}")
async def deep_research_output_get(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    pass