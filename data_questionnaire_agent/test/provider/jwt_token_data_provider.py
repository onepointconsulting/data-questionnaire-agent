from data_questionnaire_agent.model.jwt_token import JWTTokenData

def generate_token_data() -> JWTTokenData:
    return JWTTokenData(
        name="anonymous", email="anonymous@test.com", time_delta_minutes=None
    )