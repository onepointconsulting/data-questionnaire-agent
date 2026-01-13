from aiohttp import web

from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    routes,
)
from data_questionnaire_agent.service.persistence_service_prompt_async import get_prompts


@routes.options("/prompts/{language}")
async def prompts_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.get("/prompts/{language}")
async def prompts_get(request: web.Request) -> web.Response:
    language = request.match_info.get("language", "en")
    prompts = await get_prompts(language, True)
    return web.json_response(prompts, headers=CORS_HEADERS)