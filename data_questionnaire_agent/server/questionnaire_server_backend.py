import json

import aiohttp
from aiohttp import web

from data_questionnaire_agent.model.global_configuration import (
    GlobalConfiguration,
    GlobalConfigurationProperty,
)
from data_questionnaire_agent.model.jwt_token import JWTTokenData
from data_questionnaire_agent.server.server_support import (
    CORS_HEADERS,
    get_cors_headers_with_credentials,
    handle_error,
    routes,
)
from data_questionnaire_agent.service.jwt_token_service import generate_token
from data_questionnaire_agent.service.persistence_service_async import (
    select_global_configuration,
    update_global_configuration,
)
from data_questionnaire_agent.service.persistence_service_questions_async import (
    delete_question,
    insert_question,
    select_question_and_suggestions,
    update_question,
)

SUPPORTED_LANGUAGES = ["en", "de"]


@routes.options("/admin/login")
async def admin_login_options(request: web.Request) -> web.Response:
    return web.json_response(
        {"message": "Accept all hosts"},
        headers=get_cors_headers_with_credentials(request),
    )


@routes.post("/admin/login")
async def admin_login(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"access_token": str(access_token)}:
                user_info = {"name": "", "email": ""}
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}",
                        headers={
                            "Authorization": f"Bearer {access_token}",
                            "Accept": "application/json",
                        },
                    ) as response:
                        user_info = await response.json()
                        if response.status == 200:
                            user_info = {
                                "name": user_info["name"],
                                "email": user_info["email"],
                            }
                        else:
                            raise web.HTTPInternalServerError(
                                text="Failed to get user info",
                                headers=get_cors_headers_with_credentials(request),
                            )
                jwt_token = await generate_token(
                    JWTTokenData(
                        name=user_info["name"],
                        email=user_info["email"],
                        time_delta_minutes=60 * 24,  # 24 hours
                    )
                )
                if jwt_token is None:
                    raise web.HTTPInternalServerError(
                        text="Failed to generate token",
                        headers=get_cors_headers_with_credentials(request),
                    )
                return web.json_response(
                    {
                        "access_token": jwt_token.token,
                    },
                    headers=get_cors_headers_with_credentials(request),
                )

    return await handle_error(process, request=request)


@routes.options("/protected/global_configuration")
async def global_configuration_options(request: web.Request) -> web.Response:
    return web.json_response(
        {"message": "Accept all hosts"},
        headers=get_cors_headers_with_credentials(request),
    )


@routes.get("/protected/global_configuration")
async def global_configuration(request: web.Request) -> web.Response:
    async def process(_: web.Request):
        global_configuration: GlobalConfiguration = await select_global_configuration()
        return web.json_response(
            global_configuration.model_dump(), headers=CORS_HEADERS
        )

    return await handle_error(process, request=request)


def generate_cors_response(message: str = "Accept all hosts") -> web.Response:
    return web.json_response({"message": message}, headers=CORS_HEADERS)


@routes.options("/protected/update_global_configuration")
async def update_global_configuration_options(request: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all requests"}, headers=get_cors_headers_with_credentials(request))


@routes.post("/protected/update_global_configuration")
async def update_global_configuration_web(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        properties: list[GlobalConfigurationProperty] = []
        for entry in json_content:
            key, value = entry["config_key"], entry["config_value"]
            properties.append(GlobalConfigurationProperty(config_key=key, config_value=str(value)))
        gc = GlobalConfiguration(properties=properties)
        updated = await update_global_configuration(gc)
        return web.json_response({"updated": updated}, headers=get_cors_headers_with_credentials(request))

    return await handle_error(process, request=request)


@routes.options("/protected/questions/{language}")
async def read_questions_options(request: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all requests"}, headers=get_cors_headers_with_credentials(request))


@routes.get("/protected/questions/{language}")
async def read_questions(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        lang_response = process_language(request)
        if isinstance(lang_response, web.Response):
            return lang_response
        question_and_suggestions = await select_question_and_suggestions(lang_response)
        return web.json_response(question_and_suggestions.dict(), headers=get_cors_headers_with_credentials(request))

    return await handle_error(process, request=request)


@routes.options("/protected/questions/update")
async def update_questions_options(request: web.Request) -> web.Response:
    return web.json_response({"message": "Accept all requests"}, headers=get_cors_headers_with_credentials(request))


@routes.post("/protected/questions/update")
async def update_questions(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case [
                {
                    "id": int(id),
                    "question": str(question),
                    "language": str(language_code),
                },
                *_,
            ]:
                rowcount = 0
                for entry in json_content:
                    match entry:
                        case {
                            "id": id,
                            "question": question,
                            "suggestions": list(suggestions),
                        }:
                            if id > 0:
                                rowcount += await update_question(
                                    id, question, suggestions
                                )
                            else:
                                id = await insert_question(
                                    question, language_code, suggestions
                                )
                                if id > rowcount:
                                    rowcount += 1
                        case _:
                            return web.Response(
                                text=json.dumps({"error": """Wrong JSON format: Expected 'id' and 'question' keys in JSON."""}),
                                status=400,
                                content_type="application/json",
                                headers=get_cors_headers_with_credentials(request),
                            )
                return web.json_response({"updated": rowcount}, headers=get_cors_headers_with_credentials(request))
            case _:
                return send_rest_error(
                    """Wrong JSON format: Expected list with objects with'id' and 'question' keys in JSON.""",
                    400,
                )

    return await handle_error(process, request=request)


@routes.options("/protected/questions/create")
async def create_question_options(_: web.Request) -> web.Response:
    return generate_cors_response()


@routes.post("/protected/questions/create")
async def create_question(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {
                "question": str(question),
                "suggestions": list(suggestions),
                "language_code": str(language_code),
            }:
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


# Delete question endpoint delete_question


@routes.options("/protected/questions/delete")
async def delete_question_options(_: web.Request) -> web.Response:
    return generate_cors_response()


@routes.delete("/protected/questions/delete")
async def delete_question_process(request: web.Request) -> web.Response:
    async def process(request: web.Request):
        json_content = await request.json()
        match json_content:
            case {"id": int(id)}:
                count = await delete_question(id)
                return web.json_response({"deleted": count}, headers=CORS_HEADERS)
            case _:
                return send_rest_error(
                    """Wrong JSON format: Expected 'id' key in JSON.""",
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
