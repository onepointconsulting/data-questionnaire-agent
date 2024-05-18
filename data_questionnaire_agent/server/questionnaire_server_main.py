import asyncio

from aiohttp import web
from data_questionnaire_agent.config import websocket_cfg
from data_questionnaire_agent.config import web_server_cfg
from data_questionnaire_agent.server.questionnaire_server import app, routes


async def get_index(request: web.Request) -> web.Response:
    print("get_index")
    return web.FileResponse(web_server_cfg.ui_folder / "index.html")


if __name__ == "__main__":
    for i in range(10):
        app.router.add_get(f"/{i}", get_index)
    app.add_routes(routes)
    app.router.add_static("/", path=web_server_cfg.ui_folder.as_posix(), name="ui")
    loop = asyncio.new_event_loop()

    web.run_app(
        app,
        host=websocket_cfg.websocket_server,
        port=websocket_cfg.websocket_port,
        loop=loop,
    )