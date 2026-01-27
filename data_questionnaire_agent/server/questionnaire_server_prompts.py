from aiohttp import web

from data_questionnaire_agent.server.server_support import (
    get_cors_headers_with_credentials,
    routes,
)
from data_questionnaire_agent.service.persistence_service_prompt_async import (
    get_prompts,
    update_prompt,
)


@routes.options("/protected/prompts/{language}")
async def prompts_options(request: web.Request) -> web.Response:
    return web.json_response(
        {"message": "Accept all hosts"},
        headers=get_cors_headers_with_credentials(request),
    )


@routes.get("/protected/prompts/{language}")
async def prompts_get(request: web.Request) -> web.Response:
    language = request.match_info.get("language", "en")
    # Get parameter which determines the type of prompts to return
    add_ids = request.rel_url.query.get("add_ids", "false")
    add_ids = add_ids.lower() == "true"
    prompts = await get_prompts(language, add_ids)
    return web.json_response(
        prompts, headers=get_cors_headers_with_credentials(request)
    )


@routes.options("/protected/prompts/update/{id}")
async def prompts_update_options(request: web.Request) -> web.Response:
    return web.json_response(
        {"message": "Accept all hosts"},
        headers=get_cors_headers_with_credentials(request),
    )


@routes.put("/protected/prompts/update/{id}")
async def prompts_update(request: web.Request) -> web.Response:
    id = request.match_info.get("id", "0")
    text = await request.text()
    rowcount = await update_prompt(text, id)
    if rowcount == 0:
        return web.json_response(
            {"message": "Prompt not found"},
            status=404,
            headers=get_cors_headers_with_credentials(request),
        )
    return web.json_response(
        {"message": "Prompt updated"},
        headers=get_cors_headers_with_credentials(request),
    )
