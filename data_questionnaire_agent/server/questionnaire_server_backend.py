import json

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
    select_global_configuration,
    update_global_configuration,
)
from data_questionnaire_agent.service.persistence_service_questions_async import (
    select_question_and_suggestions,
    update_question,
    insert_question
)

SUPPORTED_LANGUAGES = ["en", "de"]


@routes.get("/global_configuration")
async def global_configuration(request: web.Request) -> web.Response:
    async def process(_: web.Request):
        global_configuration: GlobalConfiguration = await select_global_configuration()
        return web.json_response(global_configuration.dict(), headers=CORS_HEADERS)

    return await handle_error(process, request=request)


@routes.options("/protected/update_global_configuration")
async def update_global_configuration_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


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
                    text="Please provide the message_lower_limit and message_upper_limit properties.",
                    headers=CORS_HEADERS,
                )

    return await handle_error(process, request=request)


@routes.get("/questions/{language}")
async def read_questions(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        lang_response = process_language(request)
        if isinstance(lang_response, web.Response):
            return lang_response
        question_and_suggestions = await select_question_and_suggestions(lang_response)
        return web.json_response(question_and_suggestions.dict(), headers=CORS_HEADERS)

    return await handle_error(process, request=request)


@routes.options("/protected/questions/update")
async def update_questions_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/protected/questions/update")
async def update_questions(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case [
                {
                    "id": int(id),
                    "question": str(question),
                },
                *_,
            ]:
                rowcount = 0
                for entry in json_content:
                    match entry:
                        case {"id": id, "question": question}:
                            rowcount += await update_question(
                                id, question, entry["suggestions"]
                            )
                        case _:
                            return send_rest_error(
                                """Wrong JSON format: Expected 'id' and 'question' keys in JSON.""",
                                400,
                            )
                return web.json_response({"updated": rowcount}, headers=CORS_HEADERS)
            case _:
                return send_rest_error(
                    """Wrong JSON format: Expected list with objects with'id' and 'question' keys in JSON.""",
                    400,
                )

    return await handle_error(process, request=request)


@routes.options("/protected/questions/create")
async def create_question_options(_: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all hosts"}, headers=CORS_HEADERS)


@routes.post("/protected/questions/create")
async def create_question(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"question": str(question), "suggestions": list(suggestions), "language_code": str(language_code)}:
                # save the suggestions and question to the database.
                id = await insert_question(question, language_code, suggestions)
                if id is None:
                    return send_rest_error(
                        """Failed to insert question in database.""",
                        500,
                    )
                return web.json_response(
                    {"id": id, "question": question, "suggestions": suggestions},
                    headers=CORS_HEADERS,
                )
            case _:
                return send_rest_error(
                    """Wrong JSON format: expected list with objects and 'question' and 'suggestions' keys in JSON.""",
                    400,
                )

    return await handle_error(process, request=request)


def process_language(request: web.Request) -> str | web.Response:
    language = request.match_info.get("language")
    if language not in SUPPORTED_LANGUAGES:
        return send_rest_error(
            f"Invalid langguage: {language}. Available languages: {SUPPORTED_LANGUAGES}",
            400,
        )
    return language


def send_rest_error(error_message: str, error_code) -> web.Response:
    return web.Response(
        text=json.dumps({"error": error_message}),
        status=400,
        content_type="application/json",
        headers=CORS_HEADERS,
    )
