from typing import Optional

import secrets
import jwt
import time
from datetime import timedelta, datetime, timezone

from ulid import ULID

from data_questionnaire_agent.config import jwt_token_cfg
from data_questionnaire_agent.model.jwt_token import JWTToken
from data_questionnaire_agent.service.persistence_service_async import insert_jwt_token


def generate_secret() -> str:
    return secrets.token_hex(20)


async def generate_token(name: str, email: str, time_delta_minutes: Optional[int]) -> Optional[str]:
    payload = {"sub": str(ULID()), "name": name, "iat": int(time.time())}
    if time_delta_minutes is not None:
        payload['exp'] = datetime.now(timezone.utc) + timedelta(seconds=time_delta_minutes)
    token = jwt.encode(payload, jwt_token_cfg.secret, jwt_token_cfg.algorithm)
    jwt_token = JWTToken(email=email, token=token)
    id = await insert_jwt_token(jwt_token)
    if id is None:
        return None
    return jwt_token


if __name__ == "__main__":
    import asyncio

    print(generate_secret())

    print(asyncio.run(generate_token("Gil", "gil.fernandes@gmail.com", 60)))
