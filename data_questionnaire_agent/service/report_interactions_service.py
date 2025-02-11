import asyncio
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from data_questionnaire_agent.config_support import create_db_conn_str

alternate_env_file = Path(__file__) / "../../../.env_report"
assert (
    alternate_env_file.exists()
), f"The environment file {alternate_env_file} does not exist."
load_dotenv(dotenv_path=alternate_env_file)
conn_str = create_db_conn_str()

from data_questionnaire_agent.server.questionnaire_server import (
    query_questionnaire_advices,
)
from data_questionnaire_agent.service.html_generator import generate_pdf_from
from data_questionnaire_agent.service.query_support import select_from
from data_questionnaire_agent.service.report_aggregation_main_service import (
    aggregate_reports_main,
)


def create_exclusion_list(exclusions: list[str]) -> str:
    return ",".join([f"'{s}'" for s in exclusions])


async def create_usage_report(exclusion_ids: list[str]) -> pd.DataFrame | None:
    exclusion_str = create_exclusion_list(exclusion_ids)
    sql = f"""select sc.session_id, t.email, qs.question, qs.answer, qs.final_report, created_at, updated_at from tb_session_configuration sc
inner join tb_jwt_token t on sc.config_value = t.jwt_token
inner join tb_questionnaire_status qs on qs.session_id = sc.session_id
where t.email ilike '%%clustre.com' and (qs.answer is not null or qs.final_report is true) and qs.session_id not in ({exclusion_str}) order by created_at"""

    res = await select_from(sql, {}, conn_str)
    if res is None:
        return None
    frame_data = []
    for r in res:
        session_id = r[0]
        email = r[1]
        question = r[2]
        answer = r[3]
        final_report = r[4]
        created_at = r[5]
        updated_at = r[6]
        data = {
            "session_id": session_id,
            "email": email,
            "question": question,
            "answer": answer,
            "final_report": final_report,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        frame_data.append(data)
    return pd.DataFrame(data=frame_data)


async def create_aggregate_report(tokens: list[str]) -> Path:
    aggregation_report_path = await aggregate_reports_main(
        tokens=tokens, email_list=[], language="en", final_report=False
    )
    return aggregation_report_path


async def interactions_report(exclusion_ids: list[str]) -> pd.DataFrame | None:
    exclusion_str = create_exclusion_list(exclusion_ids)
    sql = f"""select * from
(select t.email, sc.session_id, count(*), min(created_at) min_created, max(created_at) max_created from tb_session_configuration sc
inner join tb_jwt_token t on sc.config_value = t.jwt_token
inner join tb_questionnaire_status qs on qs.session_id = sc.session_id
where t.id > 100 and qs.session_id not in ({exclusion_str})
group by sc.session_id, t.email
order by 5, count(*)) q where max_created > '2025-01-15'"""
    res = await select_from(sql, {}, conn_str)
    if res is None:
        return None
    frame_data = []
    for r in res:
        email = r[0]
        session_id = r[1]
        count = r[2]
        min_created = r[3]
        max_created = r[4]
        data = {
            "email": email,
            "session_id": session_id,
            "count": count,
            "min_created": min_created,
            "max_created": max_created,
        }
        frame_data.append(data)
    return pd.DataFrame(data=frame_data)


async def regenerate_pdfs(session_ids: list[str]) -> list[Path]:
    pdfs = []
    for session_id in session_ids:
        questionnaire, advices = await query_questionnaire_advices(session_id)
        report_path = generate_pdf_from(questionnaire, advices, "en")
        pdfs.append(report_path)
    return pdfs


if __name__ == "__main__":
    import shutil

    clustre_folder = Path("clustre")
    if not clustre_folder.exists():
        clustre_folder.mkdir(parents=True, exist_ok=True)

    selected_jwts = [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaN1MzMTlHMlNGOUtaMk1EMTZXQyIsIm5hbWUiOiJCYXJyeSAgR3JlZW4iLCJpYXQiOjE3MzY4NzA2OTh9.qPBnlFtpxx0Gd8ZN0weDCLHOYo8nRIJmzXErCTfDkJ0",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaN1dES1JBS0NCUlI0NTk2R0M0RyIsIm5hbWUiOiJKYW1lcyAgQmVuZm9yZCIsImlhdCI6MTczNjg3MDY5OH0.yDmlJTY6GxtkH-hIXGFG9TH544OpzYPBxvMTuu6cpUc",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaN1lROEg4WDNWNDZBUUNOS0E4RyIsIm5hbWUiOiJTaW1vbiBCdXJmb290IiwiaWF0IjoxNzM2ODcwNjk4fQ.9IobxqdhL1I8TYv5SlswBJkurAN8k8NPZCtbJeb72LI",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaODk1WUo5QTdITUs2U0Y5OTJOSCIsIm5hbWUiOiJHYWJlIEFybmV0dCIsImlhdCI6MTczNjg3MDY5OX0.w0yzxgqtCH38hxmIFkFKN5bO5XIW4RZ-7N88ELQEQUc",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOEQ1UVpEWlBaMzQwQTRYMzhBQiIsIm5hbWUiOiJTaW1vbiBIYXl0ZXIiLCJpYXQiOjE3MzY4NzA2OTl9.krYkD_vbN0P1ztSlyHY1GlW5-Yg81MXrqjulZdNnNbg",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOFJDUVdGVkNYSkdGQVQ0UktFWiIsIm5hbWUiOiJQYXVsICBNY0FudWx0eSIsImlhdCI6MTczNjg3MDY5OX0.xicjypvvDNzIHk3WQowe8UkRvoRH0HbwearfTA9p_0E",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOFZBVzZEQUVQMVQwQVM5UDNWMSIsIm5hbWUiOiJOemF1IE11aW5kZSIsImlhdCI6MTczNjg3MDY5OX0.W-lAENIN9RIxG3At3VeKnusIIZqg7jA3DEM_wvcv51w",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpISlJaOTRIUUZHWTFZWFg5NjJCMzBGSyIsIm5hbWUiOiJBYmhpbmF3IFNpbmdoIiwiaWF0IjoxNzM2ODcwNzAwfQ.nzXRKBZ7T0zF5Lo6GrDMSghToMbpzxPUKk4NfGGUH4Q",
    ]

    exclusion_ids = [
        "01JHMT1J1MP0F5VEE81JH509ZR",
        "01JHMT2YPD9T7ZXV5195WT39AQ",
        "01JHMTX54679QN5H5PT1AY4SX9",
        "01JHN1H7J50TMJA784Q8HD9CM3",
        "01JJP8N47XEG8X58MHH0Z3NPXX",
        "01JK8F4YTXFX2TSKMR8AV614HN",
    ]

    def execute_create_usage_report():
        df: pd.DataFrame = asyncio.run(create_usage_report(exclusion_ids))
        assert df is not None, "There is not dataframe"
        df.to_excel(clustre_folder / "meaningfull_interactions_report.xlsx")

    def execute_create_aggregate_report():
        report_path = asyncio.run(create_aggregate_report(selected_jwts))
        shutil.copy(report_path, clustre_folder / report_path.name)

    def execute_interactions_report():
        df = asyncio.run(interactions_report(exclusion_ids))
        df.to_excel(clustre_folder / "interactions_report.xlsx")

    def execute_regenerate_pdfs():
        df: pd.DataFrame = asyncio.run(create_usage_report(exclusion_ids))
        session_ids = list(
            df[df["final_report"]]["session_id"].to_dict().values()
        )
        paths = asyncio.run(regenerate_pdfs(session_ids))
        for path in paths:
            print(path)

    # execute_create_usage_report()
    # execute_interactions_report()
    # execute_create_aggregate_report()
    execute_regenerate_pdfs()
