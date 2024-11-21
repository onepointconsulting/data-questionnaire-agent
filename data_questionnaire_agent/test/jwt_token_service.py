from data_questionnaire_agent.service.jwt_token_service import decode_token


def test_decode_token():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUo3RzRHMlEyRUVTWTY2Q1BHUjZFR042SCIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MjYwNDQ3MDMsImV4cCI6MTcyNjA0NDc2M30.2IJ_DoSQ8hyU4DU3lgXZduYPvoaAgxP1WKqTHbphI8Y"
    decoded = decode_token(token)
    assert decoded is not None, "Decoded should not be none."
