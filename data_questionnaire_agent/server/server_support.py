from typing import Awaitable
from aiohttp import web

from data_questionnaire_agent.log_init import logger

CORS_HEADERS = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"}

routes = web.RouteTableDef()

async def handle_error(fun: Awaitable, **kwargs) -> any:
    try:
        return await fun(kwargs["request"])
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise web.HTTPBadRequest(
            text="Please make sure the JSON body is available and well formatted."
        )