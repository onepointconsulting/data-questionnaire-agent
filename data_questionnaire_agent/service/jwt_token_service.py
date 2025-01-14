import asyncio
import secrets
import time
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional

import jwt
import pandas as pd
from ulid import ULID

from data_questionnaire_agent.config import cfg, jwt_token_cfg
from data_questionnaire_agent.model.jwt_token import JWTToken, JWTTokenData
from data_questionnaire_agent.service.persistence_service_async import insert_jwt_token
from data_questionnaire_agent.log_init import logger

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
    col_dwise = "D-Wise"
    data = [
        {
            col_email: t.email,
            col_token: t.token,
            col_dwell: f"{jwt_token_cfg.dwell_url}?id={t.token}",
            col_dwise: f"{jwt_token_cfg.dwise_url}?id={t.token}",
        }
        for t in generated_tokens
    ]
    df = pd.DataFrame(data=data, columns=[col_email, col_token, col_dwell, col_dwise])
    csv = cfg.jwt_gen_folder / f"{str(ULID())}.csv"
    df.to_csv(csv)
    return csv


async def generate_from_file(excel_file: Path) -> Path:
    assert excel_file.name.lower().endswith(".xlsx"), "The only support format is xlsx."
    df = pd.read_excel(excel_file)
    cols = df.columns
    first_name_col = cols[0]
    last_name_col = cols[1]
    company_col = cols[2]
    def remove_bad_chars(orig: str):
        return re.sub(r"\W+", "", orig.lower())
    token_list = []
    for i, (first_name, last_name, company) in enumerate(zip(df[first_name_col], df[last_name_col], df[company_col])):
        full_name = f"{first_name} {last_name}"
        email = f"{remove_bad_chars(full_name)}@{remove_bad_chars(company)}.clustre.com"
        token = await generate_token(JWTTokenData(name=full_name, email=email, time_delta_minutes=None))
        if token:
            token_list.append({"First name": first_name, "Last name": last_name, "Company": company, "Personal link": f"https://clustre-d-well.onepointltd.ai/0?id={token.token}", "Sent": False})
        else:
            logger.error(f"Failed to generate token for {full_name}")
    token_df = pd.DataFrame(token_list)
    result_path = excel_file.parent/f"{excel_file.stem}_tokens.xlsx"
    token_df.to_excel(result_path)
    return result_path


def generate_from_file_cmdline():
    import sys
    args = sys.argv
    if len(args) < 2:
        sys.stderr.write("Please enter the excel file from which to import the entries.")
        return
    excel_file_str = args[1]
    excel_file = Path(excel_file_str)
    token_file = asyncio.run(generate_from_file(excel_file))
    print("Generated file", token_file)


if __name__ == "__main__":

    def generate_jwt():
        print(generate_secret())
        data = JWTTokenData(name="Gil", email="test.test@test.com", time_delta_minutes=40)
        jwt_token = asyncio.run(generate_token(data))
        print(jwt_token)
        assert jwt_token is not None
        print(asyncio.run(decode_token(jwt_token.token)))

    generate_from_file_cmdline()
