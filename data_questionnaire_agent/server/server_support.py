from typing import Awaitable

from aiohttp import web

from data_questionnaire_agent.log_init import logger

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
}


def get_cors_headers_with_credentials(request: web.Request) -> dict:
    """
    Get CORS headers that work with credentials.
    When credentials are involved, Access-Control-Allow-Origin cannot be "*".
    It must be the actual origin of the request.
    """
    origin = request.headers.get("Origin")
    if not origin:
        # Fallback to "*" if no origin (shouldn't happen with credentials, but handle gracefully)
        origin = "*"

    # Get the requested headers from the preflight request, or use common defaults
    requested_headers = request.headers.get("Access-Control-Request-Headers")
    if requested_headers:
        # Echo back what the browser requested
        allowed_headers = requested_headers
    else:
        # Default headers that are commonly needed
        allowed_headers = "Content-Type, Authorization, Accept"

    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Headers": allowed_headers,
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Max-Age": "86400",
    }


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
