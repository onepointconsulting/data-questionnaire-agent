import asyncio

from aiohttp import web

from data_questionnaire_agent.config import web_server_cfg, websocket_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.server.questionnaire_server import (
    MAX_SESSION_STEPS,
    app,
    routes,
)
from data_questionnaire_agent.server.questionnaire_server_backend import (
    routes as config_routes,
)
from data_questionnaire_agent.server.questionnaire_server_consultants import (
    routes as consultant_routes,
)
from data_questionnaire_agent.server.questionnaire_server_deep_research import (
    routes as deep_research_routes,
)
from data_questionnaire_agent.server.questionnaire_server_prompts import (
    routes as prompts_routes,
)

assert config_routes == routes
assert consultant_routes == routes
assert deep_research_routes == routes
assert prompts_routes == routes

FILE_INDEX = "index.html"
PATH_INDEX = web_server_cfg.ui_folder / FILE_INDEX
INDEX_LINKS = ["/", "/admin"]


@web.middleware
async def admin_oauth_token_middleware(request, handler):
    # Only intercept the "/admin" path (possibly with trailing slash)
    if request.path == "/admin" or request.path.rstrip("/") == "/admin":
        # Try to extract access token from query, header, or cookies
        token = None

        # 1. Check Authorization header: "Bearer <token>"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):].strip()

        # 2. Check for "access_token" in query params if not already found
        if not token:
            token = request.rel_url.query.get("access_token")

        # 3. Check for "access_token" in cookies if not already found
        if not token:
            token = request.cookies.get("access_token")

        # Attach token info to request for downstream use (if needed)
        if token:
            request["google_oauth_access_token"] = token
        else:
            request["google_oauth_access_token"] = None

    # Continue processing request
    return await handler(request)

# Register the middleware to the app
app.middlewares.append(admin_oauth_token_middleware)



async def get_index(_: web.Request) -> web.Response:
    return web.FileResponse(PATH_INDEX)


def run_server():
    for i in range(MAX_SESSION_STEPS):
        app.router.add_get(f"/{i}", get_index)
    for url in INDEX_LINKS:
        app.router.add_get(url, get_index)
    app.add_routes(routes)
    app.router.add_static(
        "/images", path=web_server_cfg.images_folder.as_posix(), name="images"
    )
    app.router.add_static("/", path=web_server_cfg.ui_folder.as_posix(), name="ui")
    loop = asyncio.new_event_loop()

    logger.info(
        f"Running server on {websocket_cfg.websocket_server}:{websocket_cfg.websocket_port}"
    )

    web.run_app(
        app,
        host=websocket_cfg.websocket_server,
        port=websocket_cfg.websocket_port,
        loop=loop,
    )


if __name__ == "__main__":
    run_server()
