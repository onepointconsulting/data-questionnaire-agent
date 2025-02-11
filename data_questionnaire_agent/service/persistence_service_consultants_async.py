from consultant_info_generator.model import Consultant
from psycopg import AsyncCursor

from data_questionnaire_agent.service.query_support import create_cursor


async def __process_simple_operation(sql: str, skill: str) -> int:
    async def process(cur: AsyncCursor):
        await cur.execute(sql, {"skill": skill})
        return cur.rowcount

    return await create_cursor(process, True)


async def upsert_skill(skill: str) -> int:
    sql = """
INSERT INTO TB_SKILL (SKILL_NAME) VALUES (%(skill)s) ON CONFLICT (SKILL_NAME) DO NOTHING;
"""
    return await __process_simple_operation(sql, skill)


async def delete_skill(skill: str) -> int:
    sql = """
DELETE FROM TB_SKILL WHERE SKILL_NAME = %(skill)s
"""
    return await __process_simple_operation(sql, skill)


async def save_consultant(consultant: Consultant) -> int | None:
    async def process(cur: AsyncCursor):
        sql = """
INSERT INTO TB_CONSULTANT(GIVEN_NAME, SURNAME, EMAIL, CV, INDUSTRY_NAME, GEO_LOCATION, LINKEDIN_PROFILE_URL)
VALUES(%(given_name)s, %(surname)s, %(email)s, %(cv)s, %(industry_name)s, %(location)s, %(linkedin_profile_url)s)
ON CONFLICT (EMAIL) DO UPDATE SET GIVEN_NAME=%(given_name)s, SURNAME=%(surname)s, EMAIL=%(email)s, CV=%(cv)s, INDUSTRY_NAME=%(industry_name)s, 
GEO_LOCATION=%(location)s, LINKEDIN_PROFILE_URL=%(linkedin_profile_url)s, UPDATED_AT=CURRENT_TIMESTAMP RETURNING ID;
"""
        await cur.execute(
            sql,
            {
                "given_name": consultant.given_name,
                "surname": consultant.surname,
                "email": consultant.email,
                "cv": consultant.cv,
                "industry_name": consultant.industry_name,
                "location": consultant.geo_location,
                "linkedin_profile_url": consultant.linkedin_profile_url,
            },
        )
        rows = await cur.fetchone()
        if rows is None or len(rows) == 0:
            return None
        consultant_id = rows[0]
        sql = """
DELETE FROM TB_CONSULTANT_SKILL WHERE CONSULTANT_ID = %(consultant_id)s
"""
        await cur.execute(sql, {"consultant_id": consultant_id})
        sql = """
INSERT INTO TB_SKILL(SKILL_NAME) VALUES(%(skill)s)
ON CONFLICT (SKILL_NAME) DO NOTHING
"""
        for skill in consultant.skills:
            await cur.execute(sql, {"skill": skill.name})
        
        sql = """
INSERT INTO TB_CONSULTANT_SKILL(CONSULTANT_ID, SKILL_ID) VALUES(%(consultant_id)s, (SELECT ID from TB_SKILL WHERE SKILL_NAME = %(skill_name)s))
ON CONFLICT (CONSULTANT_ID, SKILL_ID) DO NOTHING
"""
        for skill in consultant.skills:
            await cur.execute(sql, {"consultant_id": consultant_id, "skill_name": skill.name})

    return await create_cursor(process, True)


async def delete_consultant(consultant: Consultant) -> int:
    async def process(cur: AsyncCursor):
        sql = """
DELETE FROM TB_CONSULTANT WHERE EMAIL=%(email)s
"""
        await cur.execute(sql, {"email": consultant.email})
        return cur.rowcount

    return await create_cursor(process, True)
