from aiohttp import web

from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    extract_session,
    routes,
)
from data_questionnaire_agent.service.persistence_deep_research_async import read_deep_research

@routes.options("/deep_research/output/{session_id}")
async def deep_research_output_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.get("/deep_research/output/{session_id}")
async def deep_research_output_get(request: web.Request) -> web.Response:
    session_id = extract_session(request)
    deep_research_outputs = await read_deep_research(session_id)
    return web.json_response(deep_research_outputs.model_dump(), headers=CORS_HEADERS)