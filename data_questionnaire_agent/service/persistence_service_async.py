from typing import List, Union

from psycopg import AsyncConnection, AsyncCursor

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.model.global_configuration import (
    GlobalConfiguration,
    GlobalConfigurationProperty,
)
from data_questionnaire_agent.model.jwt_token import JWTToken
from data_questionnaire_agent.model.languages import DEFAULT_LANGUAGE
from data_questionnaire_agent.model.ontology_schema import Ontology
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.model.question_suggestion import (
    PossibleAnswers,
    QuestionSuggestion,
)
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.session_configuration import (
    DEFAULT_CHAT_TYPE,
    DEFAULT_SESSION_STEPS,
    SESSION_CHAT_TYPE,
    SESSION_STEPS_CONFIG_KEY,
    SESSION_STEPS_LANGUAGE_KEY,
    SessionConfiguration,
    SessionConfigurationEntry,
    SessionProperties,
)
from data_questionnaire_agent.service.persistence_service_context_documents import read_context_documents
from data_questionnaire_agent.service.query_support import (
    create_cursor,
    select_from,
    use_connection,
)


async def select_questionnaire_statuses(session_id: str) -> List[QuestionnaireStatus]:
    res = await select_from(
        """SELECT S.ID,
	S.SESSION_ID,
	QUESTION,
	ANSWER,
	FINAL_REPORT,
	CREATED_AT,
	UPDATED_AT,
	C.CONFIG_VALUE AS LANGUAGE,
    CLARIFICATION,
    QUESTION_ID
FROM TB_QUESTIONNAIRE_STATUS S
INNER JOIN PUBLIC.TB_SESSION_CONFIGURATION C ON S.SESSION_ID = C.SESSION_ID
AND C.CONFIG_KEY = 'session-language'
WHERE S.SESSION_ID = %(session_id)s
ORDER BY ID ASC""",
        {
            "session_id": session_id,
        },
    )
    ID = 0
    SESSION_ID = 1
    QUESTION = 2
    ANSWER = 3
    FINAL_REPORT = 4
    CREATED_AT = 5
    UPDATED_AT = 6
    CLARIFICATION = 8
    QUESTION_ID = 9
    final_res = []
    if res is None:
        return final_res
    ids = [r[ID] for r in res]
    context_documents = await read_context_documents(ids)
    context_documents_dict = {cd.questionnaire_status_id: cd for cd in context_documents}
    for r in res:
        final_report = r[FINAL_REPORT]
        question = r[QUESTION]
        final_res.append(
            QuestionnaireStatus(
                id=r[ID],
                session_id=r[SESSION_ID],
                question=question,
                answer=r[ANSWER],
                clarification=r[CLARIFICATION],
                final_report=final_report,
                created_at=r[CREATED_AT],
                updated_at=r[UPDATED_AT],
                question_id=r[QUESTION_ID],
                relevant_documents=context_documents_dict.get(r[ID], None),
            )
        )
    return final_res


async def select_advice(session_id: str) -> str:
    res = await select_from(
        """select question from public.tb_questionnaire_status 
where session_id = %(session_id)s and final_report = true""",
        {
            "session_id": session_id,
        },
    )
    if len(res) == 0:
        return ""
    return res[0][0]


async def update_answer(session_id: str, answer: str) -> Union[int, None]:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE TB_QUESTIONNAIRE_STATUS
SET ANSWER = %(answer)s
WHERE ID = (SELECT ID FROM PUBLIC.TB_QUESTIONNAIRE_STATUS WHERE SESSION_ID = %(session_id)s ORDER BY ID DESC LIMIT 1) 
RETURNING ID
            """,
            {"session_id": session_id, "answer": answer},
        )
        rows = await cur.fetchone()
        if len(rows) == 0:
            return None
        return rows[0]

    return await create_cursor(process_save, True)


async def update_clarification(
    session_id: str, question: str, clarification: str
) -> Union[int, None]:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE TB_QUESTIONNAIRE_STATUS
SET CLARIFICATION = %(clarification)s 
WHERE SESSION_ID = %(session_id)s
	AND QUESTION = %(question)s
RETURNING ID
            """,
            {
                "session_id": session_id,
                "question": question,
                "clarification": clarification,
            },
        )
        rows = await cur.fetchone()
        if len(rows) == 0:
            return None
        return rows[0]

    return await create_cursor(process_save, True)


async def select_questionnaire(
    session_id: str, include_last: bool = True
) -> Questionnaire:
    include_last_sql = "" if include_last else " AND FINAL_REPORT != true "
    sql = f"""SELECT QUESTION, ANSWER, FINAL_REPORT, C.CONFIG_VALUE AS LANGUAGE
FROM TB_QUESTIONNAIRE_STATUS S
INNER JOIN PUBLIC.TB_SESSION_CONFIGURATION C ON S.SESSION_ID = C.SESSION_ID
AND C.CONFIG_KEY = 'session-language'
WHERE S.SESSION_ID = %(session_id)s {include_last_sql} ORDER BY S.ID"""
    res = await select_from(
        sql,
        {
            "session_id": session_id,
        },
    )
    questions = []
    for r in res:
        is_final_report = r[2]
        if not is_final_report:
            questions.append(
                QuestionAnswer(id=None, question=r[0], answer=r[1], clarification=None)
            )
        else:
            conditional_advice = ConditionalAdvice.parse_raw(r[0])
            LANGUAGE = 3
            language = r[LANGUAGE]
            questions.append(
                QuestionAnswer(
                    id=None,
                    question=conditional_advice.to_markdown(language),
                    answer=r[1],
                    clarification=None,
                )
            )

    return Questionnaire(questions=questions)


async def select_report(session_id: str) -> Union[ConditionalAdvice, None]:
    res = await select_from(
        """SELECT QUESTION
FROM TB_QUESTIONNAIRE_STATUS
WHERE SESSION_ID = %(session_id)s AND FINAL_REPORT = true limit 1""",
        {
            "session_id": session_id,
        },
    )
    if len(res) == 0:
        return None
    advice_json = res[0][0]
    return ConditionalAdvice.parse_raw(advice_json)


async def insert_questionnaire_status(
    questionnaire_status: QuestionnaireStatus,
) -> Union[QuestionnaireStatus, None]:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_QUESTIONNAIRE_STATUS (SESSION_ID, QUESTION, FINAL_REPORT, TOTAL_COST, CREATED_AT, UPDATED_AT, QUESTION_ID)
VALUES (%(session_id)s, %(question)s, %(final_report)s, %(total_cost)s, now(), now(), %(question_id)s) RETURNING ID, CREATED_AT, UPDATED_AT;
            """,
            {
                "session_id": questionnaire_status.session_id,
                "question": questionnaire_status.question,
                "answer": questionnaire_status.answer,
                "final_report": questionnaire_status.final_report,
                "total_cost": questionnaire_status.total_cost,
                "question_id": questionnaire_status.question_id,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        created_at = created_row[1]
        updated_at = created_row[2]
        return QuestionnaireStatus(
            id=created_id,
            session_id=questionnaire_status.session_id,
            question=questionnaire_status.question,
            answer=questionnaire_status.answer,
            final_report=questionnaire_status.final_report,
            total_cost=questionnaire_status.total_cost,
            created_at=created_at,
            updated_at=updated_at,
        )

    return await create_cursor(process_save, True)


async def delete_questionnaire_status(id: int) -> int:
    return await delete_from_table(id, "TB_QUESTIONNAIRE_STATUS")


async def delete_from_table(id: int, table: str) -> int:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            f"""
DELETE FROM {table} WHERE ID = %(id)s
            """,
            {"id": id},
        )
        return cur.rowcount

    return await create_cursor(process_save, True)


async def save_session_configuration(
    session_configuration: SessionConfigurationEntry,
) -> Union[SessionConfigurationEntry, None]:
    async def process_save(cur: AsyncCursor):
        session_id = session_configuration.session_id
        config_key = session_configuration.config_key
        config_value = session_configuration.config_value
        await cur.execute(
            """
INSERT INTO TB_SESSION_CONFIGURATION(SESSION_ID, CONFIG_KEY, CONFIG_VALUE)
VALUES (%(session_id)s, %(config_key)s, %(config_value)s) RETURNING ID
            """,
            {
                "session_id": session_id,
                "config_key": config_key,
                "config_value": config_value,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        return SessionConfigurationEntry(
            id=created_id,
            session_id=session_id,
            config_key=config_key,
            config_value=config_value,
        )

    return await create_cursor(process_save, True)


async def delete_session_configuration(id: int) -> int:
    return await delete_from_table(id, "TB_SESSION_CONFIGURATION")


async def select_session_configuration(session_id: str) -> SessionConfiguration:
    res = await select_from(
        """SELECT ID, SESSION_ID, CONFIG_KEY, CONFIG_VALUE
FROM PUBLIC.TB_SESSION_CONFIGURATION
WHERE SESSION_ID = %(session_id)s ORDER BY ID""",
        {
            "session_id": session_id,
        },
    )
    return SessionConfiguration(
        configuration_entries=[
            SessionConfigurationEntry(
                id=r[0], session_id=r[1], config_key=r[2], config_value=r[3]
            )
            for r in res
        ]
    )


async def has_final_report(session_id: str) -> bool:
    res = await select_from(
        """SELECT final_report FROM PUBLIC.TB_QUESTIONNAIRE_STATUS
WHERE SESSION_ID = %(session_id)s and final_report = true""",
        {
            "session_id": session_id,
        },
    )
    if res is None or len(res) == 0:
        return False
    return True if res[0][0] else False


async def update_session_steps(session_id: str, session_steps: int) -> Union[int, None]:
    async def process_update(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE TB_SESSION_CONFIGURATION SET CONFIG_VALUE = %(config_value)s
WHERE SESSION_ID = %(session_id)s AND CONFIG_KEY = %(config_key)s RETURNING ID
            """,
            {
                "session_id": session_id,
                "config_key": SESSION_STEPS_CONFIG_KEY,
                "config_value": session_steps,
            },
        )
        created_row = await cur.fetchone()
        if created_row is None:
            return None
        updated_id = created_row[0]
        return updated_id

    return await create_cursor(process_update, True)


async def delete_last_question(session_id: str) -> Union[int, None]:
    async def process_delete(cur: AsyncCursor):
        await cur.execute(
            """
DELETE FROM PUBLIC.TB_QUESTIONNAIRE_STATUS 
WHERE ID = (SELECT ID FROM PUBLIC.TB_QUESTIONNAIRE_STATUS WHERE SESSION_ID = %(session_id)s ORDER BY ID DESC LIMIT 1)
RETURNING ID
""",
            {
                "session_id": session_id,
            },
        )
        created_row = await cur.fetchone()
        if created_row is None or len(created_row) == 0:
            return None
        updated_id = created_row[0]
        return updated_id

    return await create_cursor(process_delete, True)


async def select_current_session_steps_and_language(
    session_id: str,
) -> SessionProperties:
    res = await select_from(
        f"""
SELECT CONFIG_KEY, CONFIG_VALUE
FROM TB_SESSION_CONFIGURATION
WHERE SESSION_ID = %(session_id)s
        AND CONFIG_KEY in ('{SESSION_STEPS_CONFIG_KEY}', '{SESSION_STEPS_LANGUAGE_KEY}', '{SESSION_CHAT_TYPE}')
""",
        {"session_id": session_id},
    )
    default_values = (DEFAULT_SESSION_STEPS, DEFAULT_LANGUAGE, DEFAULT_CHAT_TYPE)
    if len(res) == 0 or len(res[0]) == 0 or res[0][0] is None:
        return default_values
    steps = default_values[0]
    language = default_values[1]
    chat_type = default_values[2]
    try:
        for r in res:
            key = r[0]
            if key == SESSION_STEPS_CONFIG_KEY:
                steps = int(r[1]) if r[1] != "None" else steps
            elif key == SESSION_STEPS_LANGUAGE_KEY:
                language = str(r[1])
            elif key == SESSION_CHAT_TYPE:
                chat_type = str(r[1])
    except:
        logger.exception("Cannot select current session steps")
    return SessionProperties(
        session_steps=steps, session_language=language, chat_type=chat_type
    )


async def save_report(
    session_id: str, conditional_advice: ConditionalAdvice, total_cost: float = 0
) -> int:
    conditional_advice_json = conditional_advice.json()

    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_QUESTIONNAIRE_STATUS(SESSION_ID, QUESTION, FINAL_REPORT, CREATED_AT, UPDATED_AT, TOTAL_COST)
VALUES (%(session_id)s, %(question)s, TRUE, NOW(), NOW(), %(total_cost)s) RETURNING ID
            """,
            {
                "session_id": session_id,
                "question": conditional_advice_json,
                "total_cost": total_cost,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        return created_id

    return await create_cursor(process_save, True)


async def insert_questionnaire_status_suggestions(
    questionnaire_status_id: id, question_answer: QuestionAnswer
) -> int:
    async def insert_suggestions(conn: AsyncConnection) -> int:
        changed = 0
        async with conn.pipeline():
            for suggestion in question_answer.possible_answers:
                await conn.execute(
                    """INSERT INTO TB_QUESTIONNAIRE_STATUS_SUGGESTIONS (QUESTIONNAIRE_STATUS_ID, MAIN_TEXT) VALUES (%s, %s)""",
                    [questionnaire_status_id, suggestion],
                )
                changed += 1
        return changed

    return await use_connection(insert_suggestions)


async def save_ontology(session_id: str, ontology: Ontology) -> int:
    relationships_json = ontology.json()

    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_ONTOLOGY(SESSION_ID, RELATIONSHIPS)
VALUES (%(session_id)s, %(relationships)s) RETURNING ID
            """,
            {"session_id": session_id, "relationships": relationships_json},
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        return created_id

    return await create_cursor(process_save, True)


async def delete_ontology(session_id: str) -> int:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
DELETE FROM TB_ONTOLOGY WHERE SESSION_ID = %(session_id)s
            """,
            {"session_id": session_id},
        )
        return cur.rowcount

    return await create_cursor(process_save, True)


async def fetch_ontology(session_id: str) -> dict:
    res = await select_from(
        """
SELECT relationships
FROM TB_ONTOLOGY
WHERE SESSION_ID = %(session_id)s
""",
        {"session_id": session_id},
    )
    if len(res) == 0:
        return ""
    return res[0][0]


async def select_questionnaire_status_suggestions(
    questionnaire_status_id: id,
) -> List[QuestionSuggestion]:
    res = await select_from(
        """
SELECT ID, MAIN_TEXT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS
WHERE QUESTIONNAIRE_STATUS_ID = %(questionnaire_status_id)s
""",
        {"questionnaire_status_id": questionnaire_status_id},
    )
    return question_suggestion_factory(res)


async def select_last_questionnaire_status_suggestions(
    session_id: str,
) -> List[QuestionSuggestion]:
    res = await select_from(
        """
SELECT SS.ID, SS.MAIN_TEXT
FROM TB_QUESTIONNAIRE_STATUS_SUGGESTIONS SS
INNER JOIN PUBLIC.TB_QUESTIONNAIRE_STATUS QS ON QS.ID = SS.QUESTIONNAIRE_STATUS_ID
WHERE QS.SESSION_ID = %(session_id)s
	AND QS.ID =
		(SELECT MAX(ID)
			FROM TB_QUESTIONNAIRE_STATUS
			WHERE SESSION_ID = %(session_id)s)
""",
        {"session_id": session_id},
    )
    return question_suggestion_factory(res)


def question_suggestion_factory(res: list) -> List[QuestionSuggestion]:
    """
    Factory function to create a list of QuestionSuggestion objects from the result set.
    """
    ID = 0
    MAIN_TEXT = 1
    if res is None:
        return {}
    return [
        QuestionSuggestion(
            id=r[ID],
            img_src="",
            img_alt="",
            title="",
            svg_image="",
            main_text=r[MAIN_TEXT],
        )
        for r in res
    ]


async def save_confidence(
    session_id: str,
    step: int,
    confidence: ConfidenceRating,
) -> Union[ConfidenceRating, None]:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE TB_QUESTIONNAIRE_STATUS
SET CONFIDENCE_RATING = %(confidence_rating)s, CONFIDENCE_REASONING = %(confidence_reasoning)s
WHERE ID = (SELECT ID FROM PUBLIC.TB_QUESTIONNAIRE_STATUS WHERE SESSION_ID = %(session_id)s ORDER BY ID OFFSET %(step)s LIMIT 1) RETURNING ID
            """,
            {
                "session_id": session_id,
                "confidence_rating": confidence.rating if confidence else "",
                "confidence_reasoning": confidence.reasoning if confidence else "",
                "step": step,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0] if created_row is not None else -1
        return ConfidenceRating(
            id=created_id, rating=confidence.rating, reasoning=confidence.reasoning
        )

    return await create_cursor(process_save, True)


async def save_additional_suggestions(
    suggestions: PossibleAnswers, session_id: str
) -> int:
    async def process_save(cur: AsyncCursor):
        count = 0
        for suggestion in suggestions.possible_answers:
            await cur.execute(
                """
        INSERT INTO PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS(MAIN_TEXT, QUESTIONNAIRE_STATUS_ID)
        VALUES(%(main_text)s, (SELECT MAX(ID)
                    FROM TB_QUESTIONNAIRE_STATUS
                    WHERE SESSION_ID = %(session_id)s)) RETURNING ID
        """,
                {
                    "session_id": session_id,
                    "main_text": suggestion.main_text,
                },
            )
            count += cur.rowcount
        return count

    return await create_cursor(process_save, True)


async def select_confidence(
    session_id: str,
    step: int,
) -> Union[ConfidenceRating, None]:
    res = await select_from(
        """
SELECT 
    ID, 
    CASE 
        WHEN final_report = true AND QUESTION ILIKE '%%{%%' 
        THEN (QUESTION::json->'confidence'->>'rating') 
        ELSE CONFIDENCE_RATING 
    END as CONFIDENCE_RATING,
    CASE 
        WHEN final_report = true AND QUESTION ILIKE '%%{%%' 
        THEN (QUESTION::json->'confidence'->>'reasoning') 
        ELSE CONFIDENCE_REASONING 
    END as CONFIDENCE_REASONING
FROM 
    PUBLIC.TB_QUESTIONNAIRE_STATUS
WHERE 
    SESSION_ID = %(session_id)s 
ORDER BY 
    ID 
OFFSET %(step)s LIMIT 1;
""",
        {"session_id": session_id, "step": step},
    )
    ID = 0
    CONFIDENCE_RATING = 1
    CONFIDENCE_REASONING = 2
    if res is None or len(res) == 0:
        return None
    r = res[0]
    if r[CONFIDENCE_RATING] is None:
        return None
    return ConfidenceRating(
        id=r[ID], reasoning=r[CONFIDENCE_REASONING], rating=r[CONFIDENCE_RATING]
    )


async def insert_jwt_token(jwt_token: JWTToken) -> int:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_JWT_TOKEN(EMAIL, JWT_TOKEN)
VALUES(%(email)s, %(jwt_token)s) RETURNING ID
            """,
            {"email": jwt_token.email, "jwt_token": jwt_token.token},
        )
        created_row = await cur.fetchone()
        created_id = created_row[0] if created_row is not None else -1
        return created_id

    return await create_cursor(process_save, True)


async def delete_jwt_token(id: int) -> int:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
DELETE FROM TB_JWT_TOKEN WHERE ID = %(id)s
            """,
            {"id": id},
        )
        return cur.rowcount

    return await create_cursor(process_save, True)


async def check_question_exists(question: str, session_id: str) -> bool:
    res = await select_from(
        """
SELECT count(*)
FROM tb_questionnaire_status
WHERE session_id = %(session_id)s
	AND trim(lower(question)) = trim(lower(%(question)s))
""",
        {"session_id": session_id, "question": question},
    )
    r = res[0]
    return r[0] > 0


async def select_questionnaires_by_tokens(
    tokens: List[str], final_report: bool = True
) -> List[QuestionnaireStatus]:
    sql = f"""
SELECT ID,
    SESSION_ID,
	QUESTION,
	ANSWER,
	FINAL_REPORT,
	CREATED_AT,
	UPDATED_AT,
	TOTAL_COST,
	CLARIFICATION,
    QUESTION_ID
FROM TB_QUESTIONNAIRE_STATUS
WHERE SESSION_ID IN
		(SELECT DISTINCT C.SESSION_ID
			FROM TB_SESSION_CONFIGURATION C
			INNER JOIN TB_QUESTIONNAIRE_STATUS S ON S.SESSION_ID = C.SESSION_ID
			WHERE C.CONFIG_KEY = 'session-client-id'
				{f'AND C.CONFIG_VALUE = ANY(ARRAY[{",".join([f"'{t}'" for t in tokens])}])' if len(tokens) > 0 else ""}
				AND S.FINAL_REPORT = %(final_report)s)
AND (ANSWER is not null or FINAL_REPORT is true)
ORDER BY SESSION_ID, ID ASC;
"""
    logger.info("select_questionnaires_by_tokens SQL: %s", sql)
    res = await select_from(sql, {"final_report": final_report})
    ID = 0
    SESSION_ID = 1
    QUESTION = 2
    ANSWER = 3
    FINAL_REPORT = 4
    CREATED_AT = 5
    UPDATED_AT = 6
    TOTAL_COST = 7
    CLARIFICATION = 8
    QUESTION_ID = 9
    if res is None:
        return []
    return [
        QuestionnaireStatus(
            id=r[ID],
            session_id=r[SESSION_ID],
            question=r[QUESTION],
            answer=r[ANSWER],
            final_report=r[FINAL_REPORT],
            created_at=r[CREATED_AT],
            updated_at=r[UPDATED_AT],
            total_cost=r[TOTAL_COST],
            clarification=r[CLARIFICATION],
            question_id=r[QUESTION_ID],
        )
        for r in res
    ]


async def select_global_configuration() -> GlobalConfiguration:
    sql = """SELECT CONFIG_KEY, CONFIG_VALUE FROM PUBLIC.TB_GLOBAL_CONFIGURATION;"""
    res = await select_from(sql, {})
    if not res:
        return GlobalConfiguration(properties=[])
    properties = [
        GlobalConfigurationProperty(config_key=r[0], config_value=r[1]) for r in res
    ]
    return GlobalConfiguration(properties=properties)


async def update_global_configuration(
    global_configuration: GlobalConfiguration,
) -> GlobalConfiguration:
    async def process_update(cur: AsyncCursor):
        sql = """INSERT INTO public.tb_global_configuration(config_key, config_value, description, created_at)
VALUES(%(config_key)s, %(config_value)s, 'Number of messages after which the user is given the option of stopping the questionnaire before time', now())
ON CONFLICT (config_key)
DO UPDATE set config_value = %(config_value)s"""
        total_count = 0
        for prop in global_configuration.properties:
            await cur.execute(
                sql, {"config_key": prop.config_key, "config_value": prop.config_value}
            )
            total_count += cur.rowcount
        return total_count

    return await create_cursor(process_update, True)


async def update_regenerated_question(
    session_id: str, previous_question: str, new_question: str, suggestions: list[str]
) -> bool:
    async def process_update(cur: AsyncCursor):
        select_questionnaire_id = """
(SELECT ID
			FROM TB_QUESTIONNAIRE_STATUS
			WHERE SESSION_ID = %(session_id)s
			ORDER BY ID DESC
			LIMIT 1)
"""
        await cur.execute(
            f"""
UPDATE TB_QUESTIONNAIRE_STATUS
SET QUESTION = %(new_question)s, CLARIFICATION=''
WHERE ID = {select_questionnaire_id}
		
	AND QUESTION = %(previous_question)s;
""",
            {
                "session_id": session_id,
                "previous_question": previous_question,
                "new_question": new_question,
            },
        )
        first_row_count = cur.rowcount
        # Delete previous suggestions
        await cur.execute(
            f"""
DELETE FROM tb_questionnaire_status_suggestions 
WHERE questionnaire_status_id = {select_questionnaire_id}
""",
            {"session_id": session_id},
        )
        for suggestion in suggestions:
            await cur.execute(
                f"""
INSERT INTO tb_questionnaire_status_suggestions (questionnaire_status_id, main_text)
VALUES(({select_questionnaire_id}), %(suggestion)s)
""",
                {"session_id": session_id, "suggestion": suggestion},
            )
        return first_row_count == 1

    return await create_cursor(process_update, True)
