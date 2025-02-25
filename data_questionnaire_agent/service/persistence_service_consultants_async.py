from consultant_info_generator.model import Company, Consultant, Experience, Skill
from psycopg import AsyncCursor

from data_questionnaire_agent.model.consultant_rating import (
    SCORES,
    ConsultantRating,
    ConsultantRatings,
)
from data_questionnaire_agent.service.query_support import create_cursor, select_from


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

        sql = """DELETE FROM TB_CONSULTANT_SKILL WHERE CONSULTANT_ID = %(consultant_id)s"""
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
            await cur.execute(
                sql, {"consultant_id": consultant_id, "skill_name": skill.name}
            )

        company_sql = """
INSERT INTO TB_COMPANY(COMPANY_NAME) VALUES(%(company_name)s)
ON CONFLICT (COMPANY_NAME) DO NOTHING
"""
        experience_sql = """
INSERT INTO TB_CONSULTANT_EXPERIENCE(CONSULTANT_ID, TITLE, LOCATION, START_DATE, END_DATE, COMPANY_ID)
VALUES(%(consultant_id)s, %(title)s, %(location)s, %(start_date)s, %(end_date)s, (SELECT ID FROM TB_COMPANY WHERE COMPANY_NAME = %(company_name)s))
"""
        for experience in consultant.experiences:
            if experience.company:
                company_name = experience.company.name
                await cur.execute(company_sql, {"company_name": company_name})
                await cur.execute(
                    experience_sql,
                    {
                        "consultant_id": consultant_id,
                        "title": experience.title,
                        "location": experience.location,
                        "start_date": experience.start,
                        "end_date": experience.end,
                        "company_name": experience.company.name,
                    },
                )

    return await create_cursor(process, True)


async def delete_consultant(consultant: Consultant) -> int:
    async def process(cur: AsyncCursor):
        sql = """
DELETE FROM TB_CONSULTANT WHERE EMAIL=%(email)s
"""
        await cur.execute(sql, {"email": consultant.email})
        return cur.rowcount

    return await create_cursor(process, True)


async def read_consultants(offset: int = None, limit: int = None) -> list[Consultant]:
    splitter = "@@"
    offset_expression = f"OFFSET {offset}" if offset else ""
    limit_expression = f"LIMIT {limit}" if limit else ""
    consultant_sql = f"""
select C.ID, C.GIVEN_NAME, C.SURNAME, C.EMAIL, C.CV, C.INDUSTRY_NAME, C.GEO_LOCATION, C.LINKEDIN_PROFILE_URL,
string_agg(S.SKILL_NAME, '{splitter}') skills from TB_CONSULTANT C 
INNER JOIN TB_CONSULTANT_SKILL CS ON C.ID = CS.CONSULTANT_ID
INNER JOIN TB_SKILL S ON S.ID = CS.SKILL_ID
GROUP BY C.ID, C.GIVEN_NAME, C.SURNAME, C.EMAIL, C.CV, C.INDUSTRY_NAME, C.GEO_LOCATION, C.LINKEDIN_PROFILE_URL
{offset_expression} {limit_expression}
"""
    experience_sql = """
SELECT TITLE, LOCATION, START_DATE, END_DATE, CO.COMPANY_NAME FROM TB_CONSULTANT_EXPERIENCE E
INNER JOIN TB_CONSULTANT C ON C.ID = E.CONSULTANT_ID
INNER JOIN TB_COMPANY CO ON CO.ID = E.COMPANY_ID
WHERE C.ID = %(consultant_id)s
"""
    rows = await select_from(consultant_sql, {})
    consultant_id = 0
    consultant_given_name = 1
    consultant_surname = 2
    consultant_email = 3
    consultant_cv = 4
    consultant_industry_name = 5
    consultant_geo_location = 6
    consultant_linkedin_profile_url = 7
    consultant_skills = 8
    consultants = []

    experience_title = 0
    experience_location = 1
    experience_start_date = 2
    experience_end_date = 3
    experience_company = 4
    for r in rows:
        id = r[consultant_id]
        skills_str = r[consultant_skills]
        skills = [Skill(name=s) for s in skills_str.split(splitter)]
        experience_rows = await select_from(experience_sql, {"consultant_id": id})
        experiences = [
            Experience(
                title=e[experience_title],
                location=e[experience_location],
                start=e[experience_start_date],
                end=e[experience_end_date],
                company=Company(name=e[experience_company]),
            )
            for e in experience_rows
        ]
        consultants.append(
            Consultant(
                given_name=r[consultant_given_name],
                surname=r[consultant_surname],
                email=r[consultant_email],
                cv=r[consultant_cv],
                industry_name=r[consultant_industry_name],
                geo_location=r[consultant_geo_location],
                linkedin_profile_url=r[consultant_linkedin_profile_url],
                experiences=experiences,
                skills=skills,
            )
        )
    return consultants


async def save_session_consultant_ratings(
    session_id: str, consultant_ratings: ConsultantRatings
) -> int:
    async def process(cur: AsyncCursor):
        sql = """
INSERT INTO TB_SESSION_CONSULTANT_RATING(CONSULTANT_ID, SESSION_ID, REASONING, RATING, RATING_NUMBER, CREATED_AT)
VALUES((SELECT ID FROM TB_CONSULTANT WHERE LINKEDIN_PROFILE_URL = %(linkedin_profile_url)s), %(session_id)s, %(reasoning)s, %(rating)s, %(rating_number)s, CURRENT_TIMESTAMP)
"""
        counter = 0
        for cr in consultant_ratings.consultant_ratings:
            await cur.execute(
                sql,
                {
                    "linkedin_profile_url": cr.analyst_linkedin_url,
                    "session_id": session_id,
                    "rating": cr.rating,
                    "reasoning": cr.reasoning,
                    "rating_number": SCORES[cr.rating],
                },
            )
            counter += cur.rowcount
        return counter

    return await create_cursor(process, True)


async def delete_session_consultant_ratings(session_id: str) -> int:
    async def process(cur: AsyncCursor):
        sql = """
DELETE FROM TB_SESSION_CONSULTANT_RATING
WHERE SESSION_ID = %(session_id)s
"""
        await cur.execute(sql, {"session_id": session_id})
        return cur.rowcount

    return await create_cursor(process, True)


async def read_session_consultant_ratings(
    session_id: str, limit: int = 5
) -> ConsultantRatings:
    sql = """
SELECT C.GIVEN_NAME, C.SURNAME, C.LINKEDIN_PROFILE_URL, SC.REASONING, SC.RATING FROM TB_SESSION_CONSULTANT_RATING SC INNER JOIN TB_CONSULTANT C ON C.ID = SC.CONSULTANT_ID
WHERE SC.SESSION_ID = %(session_id)s ORDER BY SC.RATING_NUMBER DESC LIMIT %(limit)s
"""
    rows = await select_from(sql, {"session_id": session_id, "limit": limit})
    pos_given_name = 0
    pos_surname = 1
    pos_linkedin_profile_url = 2
    pos_reasoning = 3
    pos_rating = 4
    consultant_ratings = [
        ConsultantRating(
            analyst_name=f"{row[pos_given_name]} {row[pos_surname]}",
            analyst_linkedin_url=row[pos_linkedin_profile_url],
            reasoning=row[pos_reasoning],
            rating=row[pos_rating],
        )
        for row in rows
    ]
    return ConsultantRatings(consultant_ratings=consultant_ratings)
