import asyncio

from aiohttp import web

from data_questionnaire_agent.config import web_server_cfg, websocket_cfg
from data_questionnaire_agent.server.questionnaire_server import (
    MAX_SESSION_STEPS,
    app,
    routes,
)

FILE_INDEX = "index.html"
PATH_INDEX = web_server_cfg.ui_folder / FILE_INDEX


async def get_index(request: web.Request) -> web.Response:
    return web.FileResponse(PATH_INDEX)


def run_server():

    for i in range(MAX_SESSION_STEPS):
        app.router.add_get(f"/{i}", get_index)
    app.router.add_get("/", get_index)
    app.router.add_get("/jwt-token", get_index)
    app.add_routes(routes)
    app.router.add_static(
        "/images", path=web_server_cfg.images_folder.as_posix(), name="images"
    )
    app.router.add_static("/", path=web_server_cfg.ui_folder.as_posix(), name="ui")
    loop = asyncio.new_event_loop()
    
    web.run_app(
        app,
        host=websocket_cfg.websocket_server,
        port=websocket_cfg.websocket_port,
        loop=loop,
    )



if __name__ == "__main__":
    run_server()
