import asyncio

from data_questionnaire_agent.test.provider.jwt_token_data_provider import generate_token_data
from data_questionnaire_agent.service.jwt_token_service import (
    decode_token,
    generate_token_batch,
    generate_token_batch_file
)


def test_decode_token():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUo3RzRHMlEyRUVTWTY2Q1BHUjZFR042SCIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MjYwNDQ3MDMsImV4cCI6MTcyNjA0NDc2M30.2IJ_DoSQ8hyU4DU3lgXZduYPvoaAgxP1WKqTHbphI8Y"
    decoded = decode_token(token)
    assert decoded is not None, "Decoded should not be none."


def test_generate_token_batch():
    jwt_token_data = generate_token_data()
    amount = 5
    jwt_tokens = asyncio.run(generate_token_batch(jwt_token_data, amount))
    assert len(jwt_tokens) == amount
    for jwt_token in jwt_tokens:
        decoded = asyncio.run(decode_token(jwt_token.token))
        assert decoded is not None, "Decoded should not be none."


def test_generate_token_batch_file():
    jwt_token_data = generate_token_data()
    amount = 5
    file = asyncio.run(generate_token_batch_file(jwt_token_data, amount))
    assert file.exists(), f"Cannot find file {file}"