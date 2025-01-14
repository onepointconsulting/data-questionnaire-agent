from aiohttp import web

from data_questionnaire_agent.model.global_configuration import (
    GlobalConfiguration,
    GlobalConfigurationProperty,
)
from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    handle_error,
    routes,
)
from data_questionnaire_agent.service.persistence_service_async import (
    update_global_configuration,
)


@routes.post("/protected/update_global_configuration")
async def update_global_configuration_web(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {
                "message_lower_limit": message_lower_limit,
                "message_upper_limit": message_upper_limit,
            }:
                properties = [
                    GlobalConfigurationProperty(
                        config_key="MESSAGE_LOWER_LIMIT",
                        config_value=str(message_lower_limit),
                    ),
                    GlobalConfigurationProperty(
                        config_key="MESSAGE_UPPER_LIMIT",
                        config_value=str(message_upper_limit),
                    ),
                ]
                gc = GlobalConfiguration(properties=properties)
                updated = await update_global_configuration(gc)
                return web.json_response({"updated": updated}, headers=CORS_HEADERS)
            case _:
                raise web.HTTPBadRequest(
                    text="Please provide the message_lower_limit and message_upper_limit properties."
                )

    return await handle_error(process, request=request)
