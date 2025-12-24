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


def extract_session(request: web.Request):
    session_id = request.match_info.get("session_id", None)
    if session_id is None:
        raise web.HTTPNotFound(text="No session id specified")
    logger.info("PDF session_id: %s", session_id)
    return session_id


def extract_email(request: web.Request):
    email = request.match_info.get("email", None)
    if email is None:
        raise web.HTTPNotFound(text="No email specified")
    return email


def extract_language(request: web.Request):
    return request.rel_url.query.get("language", "en")
