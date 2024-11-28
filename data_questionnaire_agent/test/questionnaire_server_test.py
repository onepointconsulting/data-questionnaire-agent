from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import web

from data_questionnaire_agent.model.jwt_token import JWTTokenData
from data_questionnaire_agent.server.questionnaire_server import routes

CORS_HEADERS = {"Access-Control-Allow-Origin": "*"}


@pytest.fixture
def client(aiohttp_client):
    app = web.Application()
    app.add_routes(routes)
    return aiohttp_client(app)


@pytest.mark.asyncio
@patch("data_questionnaire_agent.server.questionnaire_server.generate_jwt_token")
async def test_generate_jwt_token_success(mock_generate_token, client):
    # Mock the generate_token function
    mock_generate_token.return_value = AsyncMock(
        return_value=JWTTokenData(
            name="John Doe", email="john@example.com", time_delta_minutes=30
        )
    )

    # Make a POST request with valid JSON
    json_payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "time_delta_minutes": 30,
    }
    c = await client
    resp = await c.post("/gen_jwt_token", json=json_payload)

    # Validate response
    assert resp.status == 200
    body = await resp.json()
    assert body["token"] is not None
    assert body["email"] == "john@example.com"
