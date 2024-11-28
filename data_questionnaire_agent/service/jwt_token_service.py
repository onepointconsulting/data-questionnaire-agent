import secrets
import time
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import jwt
from ulid import ULID

from data_questionnaire_agent.config import jwt_token_cfg, cfg
from data_questionnaire_agent.model.jwt_token import JWTToken, JWTTokenData
from data_questionnaire_agent.service.persistence_service_async import insert_jwt_token


def generate_secret() -> str:
    return secrets.token_hex(20)


async def generate_token(token_data: JWTTokenData) -> Optional[JWTToken]:
    name, email, time_delta_minutes = (
        token_data.name,
        token_data.email,
        token_data.time_delta_minutes,
    )
    payload = {"sub": str(ULID()), "name": name, "iat": int(time.time())}
    if time_delta_minutes is not None:
        payload["exp"] = datetime.now(timezone.utc) + timedelta(
            seconds=time_delta_minutes
        )
    token = jwt.encode(payload, jwt_token_cfg.secret, jwt_token_cfg.algorithm)
    jwt_token = JWTToken(email=email, token=token)
    id = await insert_jwt_token(jwt_token)
    if id is None:
        return None
    return jwt_token


async def decode_token(token: str) -> dict:
    return jwt.decode(token, jwt_token_cfg.secret, jwt_token_cfg.algorithm)


async def generate_token_batch(base_data: JWTTokenData, amount: int) -> List[JWTToken]:
    token_datas: List[JWTTokenData] = [
        JWTTokenData(
            name=f"{base_data.name}_{i}",
            email=f"{i}_{base_data.email}",
            time_delta_minutes=base_data.time_delta_minutes,
        )
        for i in range(amount)
    ]
    generated_tokens = []
    for token_data in token_datas:
        generated = await generate_token(token_data)
        if generated:
            generated_tokens.append(generated)
    return generated_tokens


async def generate_token_batch_file(base_data: JWTTokenData, amount: int) -> Path:
    generated_tokens = await generate_token_batch(base_data, amount)
    col_email = "email"
    col_token = "token"
    col_dwell = "D-Well"
    col_dwise = "D-Well"
    data = [{col_email: t.email, col_token: t.token, col_dwell: f"https://d-well.onepointltd.ai?id={t.token}", col_dwise: f"https://d-wise.onepointltd.ai?id={t.token}"} for t in generated_tokens]
    df = pd.DataFrame(data=data, columns=[col_email, col_token, col_dwell, col_dwise])
    csv = cfg.jwt_gen_folder/f"{str(ULID())}.csv"
    df.to_csv(csv)
    return csv


if __name__ == "__main__":
    import asyncio

    print(generate_secret())
    data = JWTTokenData(name="Gil", email="test.test@test.com", time_delta_minutes=40)
    jwt_token = asyncio.run(generate_token(data))
    print(jwt_token)
    assert jwt_token is not None
    print(asyncio.run(decode_token(jwt_token.token)))
