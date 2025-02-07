import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd

from data_questionnaire_agent.config_support import create_db_conn_str

alternate_env_file = (Path(__file__)/"../../../.env_report")
assert alternate_env_file.exists(), f"The environment file {alternate_env_file} does not exist."
load_dotenv(dotenv_path=alternate_env_file)
conn_str = create_db_conn_str()

from data_questionnaire_agent.service.report_aggregation_main_service import aggregate_reports_main
from data_questionnaire_agent.service.query_support import select_from


async def create_usage_report() -> pd.DataFrame | None:
    sql = """select sc.session_id, t.email, qs.question, qs.answer from tb_session_configuration sc
inner join tb_jwt_token t on sc.config_value = t.jwt_token
inner join tb_questionnaire_status qs on qs.session_id = sc.session_id
where t.email ilike '%%clustre.com' and qs.answer is not null;"""
    
    res = await select_from(sql, {}, conn_str)
    if res is None: return None
    frame_data = []
    for r in res:
        session_id = r[0]
        email = r[1]
        question = r[2]
        answer = r[3]
        data = {"session_id": session_id, "email": email, "question": question, "answer": answer}
        frame_data.append(data)
    return pd.DataFrame(data=frame_data)


async def create_aggregate_report(tokens: list[str]) -> Path:
    aggregation_report_path = await aggregate_reports_main(
        tokens=tokens, email_list=[], language="en", final_report=False
    )
    return aggregation_report_path


async def interactions_report() -> pd.DataFrame | None:
    sql = """select * from
(select t.email, sc.session_id, count(*), min(created_at) min_created, max(created_at) max_created from tb_session_configuration sc
inner join tb_jwt_token t on sc.config_value = t.jwt_token
inner join tb_questionnaire_status qs on qs.session_id = sc.session_id
where t.id > 100
group by sc.session_id, t.email
order by 5, count(*)) q where max_created > '2025-01-15'"""
    res = await select_from(sql, {}, conn_str)
    if res is None: return None
    frame_data = []
    for r in res:
        email = r[0]
        session_id = r[1]
        count = r[2]
        min_created = r[3]
        max_created = r[4]
        data = {"email": email, "session_id": session_id, "count": count, "min_created": min_created, "max_created": max_created}
        frame_data.append(data)
    return pd.DataFrame(data=frame_data)


if __name__ == "__main__":
    
    def execute_create_usage_report():
        db_name = os.getenv("DB_NAME")
        df: pd.DataFrame = asyncio.run(create_usage_report())
        assert df is not None, "There is not dataframe"
        df.to_excel("usage_report.xlsx")

    def execute_create_aggregate_report():
        print(asyncio.run(create_aggregate_report([
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOTRIUUZHWTFZWFg5NjJCMzBGSyIsIm5hbWUiOiJBYmhpbmF3IFNpbmdoIiwiaWF0IjoxNzM2ODcwNzAwfQ.nzXRKBZ7T0zF5Lo6GrDMSghToMbpzxPUKk4NfGGUH4Q",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaN1ZKR0JWNFFFWDMyOEVLNk5IVCIsIm5hbWUiOiJaYWNoZXJ5IEFuZGVyc29uIiwiaWF0IjoxNzM2ODcwNjk4fQ.0m3GuZ-D5iTQxyk1aUvkRxIQ20-fV2pm9Cz17l04ni8",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaN1MzMTlHMlNGOUtaMk1EMTZXQyIsIm5hbWUiOiJCYXJyeSAgR3JlZW4iLCJpYXQiOjE3MzY4NzA2OTh9.qPBnlFtpxx0Gd8ZN0weDCLHOYo8nRIJmzXErCTfDkJ0",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOEQ1UVpEWlBaMzQwQTRYMzhBQiIsIm5hbWUiOiJTaW1vbiBIYXl0ZXIiLCJpYXQiOjE3MzY4NzA2OTl9.krYkD_vbN0P1ztSlyHY1GlW5-Yg81MXrqjulZdNnNbg"
        ])))

    def execute_interactions_report():
        df = asyncio.run(interactions_report())
        df.to_excel("interactions_report.xlsx")

    execute_interactions_report()