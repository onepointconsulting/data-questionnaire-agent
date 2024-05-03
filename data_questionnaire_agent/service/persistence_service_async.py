import sys
import asyncio
from typing import Callable, Coroutine, Any, Union, List
from psycopg import AsyncCursor, AsyncConnection

from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.question_suggestion import QuestionSuggestion
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import db_cfg
from data_questionnaire_agent.toml_support import prompts
from data_questionnaire_agent.model.application_schema import (
    Questionnaire,
    QuestionAnswer,
)
from data_questionnaire_agent.model.session_configuration import (
    SESSION_STEPS_CONFIG_KEY,
    DEFAULT_SESSION_STEPS,
)
from data_questionnaire_agent.model.session_configuration import (
    SessionConfigurationEntry,
    SessionConfiguration,
)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def create_connection() -> AsyncConnection:
    return await AsyncConnection.connect(conninfo=db_cfg.db_conn_str)


async def create_cursor(func: Callable, commit=False) -> Any:
    # await asynch_pool.check()
    try:
        conn = await create_connection()
        # async with asynch_pool.connection() as conn:
        async with conn.cursor() as cur:
            return await func(cur)
    except:
        logger.exception("Could not create cursor.")
    finally:
        if conn is not None:
            if commit:
                await conn.commit()
            await conn.close()


async def use_connection(func: Coroutine, commit=True) -> any:
    try:
        conn = await create_connection()
        return await func(conn)
    except:
        logger.exception("Could not create database connection.")
    finally:
        if conn is not None:
            if commit:
                await conn.commit()
            await conn.close()


async def handle_select_func(query: str, query_params: dict):
    async def func(cur: AsyncCursor):
        await cur.execute(
            query,
            query_params,
        )
        return list(await cur.fetchall())

    return func


async def select_from(query: str, parameter_map: dict) -> list:
    handle_select = await handle_select_func(query, parameter_map)
    return await create_cursor(handle_select)


async def select_initial_question() -> str:
    res = await select_from(
        """
SELECT question FROM TB_QUESTION
ORDER BY PREFERRED_QUESTION_ORDER
LIMIT 1
""",
        {},
    )
    if len(res) == 0:
        return prompts["questionnaire"]["initial"]["question"]
    else:
        return res[0][0]


async def select_questionnaire_statuses(session_id: str) -> List[QuestionnaireStatus]:
    res = await select_from(
        """select id, session_id, question, answer, final_report, created_at, updated_at from tb_questionnaire_status
where session_id = %(session_id)s order by id asc""",
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
    final_res = []
    for r in res:
        final_report = r[FINAL_REPORT]
        question = r[QUESTION]
        if final_report:
            conditional_advice = ConditionalAdvice.parse_raw(question)
            question = conditional_advice.to_markdown()
        final_res.append(
            QuestionnaireStatus(
                id=r[ID],
                session_id=r[SESSION_ID],
                question=question,
                answer=r[ANSWER],
                final_report=final_report,
                created_at=r[CREATED_AT],
                updated_at=r[UPDATED_AT],
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


async def select_questionnaire(
    session_id: str, include_last: bool = True
) -> Questionnaire:
    include_last_sql = "" if include_last else " AND FINAL_REPORT != true "
    res = await select_from(
        f"""SELECT QUESTION, ANSWER, FINAL_REPORT
FROM TB_QUESTIONNAIRE_STATUS
WHERE SESSION_ID = %(session_id)s {include_last_sql} ORDER BY ID""",
        {
            "session_id": session_id,
        },
    )
    questions = []
    for r in res:
        is_final_report = r[2]
        if not is_final_report:
            questions.append(
                QuestionAnswer(question=r[0], answer=r[1], clarification=None)
            )
        else:
            conditional_advice = ConditionalAdvice.parse_raw(r[0])
            questions.append(
                QuestionAnswer(
                    question=conditional_advice.to_markdown(),
                    answer=r[1],
                    clarification=None,
                )
            )

    return Questionnaire(questions=questions)


async def select_report(session_id: str) -> Union[ConditionalAdvice, None]:
    res = await select_from(
        f"""SELECT QUESTION
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
INSERT INTO TB_QUESTIONNAIRE_STATUS (SESSION_ID, QUESTION, FINAL_REPORT, TOTAL_COST, CREATED_AT, UPDATED_AT)
VALUES (%(session_id)s, %(question)s, %(final_report)s, %(total_cost)s, now(), now()) RETURNING ID, CREATED_AT, UPDATED_AT;
            """,
            {
                "session_id": questionnaire_status.session_id,
                "question": questionnaire_status.question,
                "answer": questionnaire_status.answer,
                "final_report": questionnaire_status.final_report,
                "total_cost": questionnaire_status.total_cost,
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


async def select_suggestions(question: str) -> List[QuestionSuggestion]:
    res = await select_from(
        """SELECT S.id, img_src, img_alt, title, main_text FROM TB_QUESTION_SUGGESTIONS S 
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
wHERE Q.question = %(question)s
ORDER BY PREFERRED_QUESTION_ORDER""",
        {
            "question": question,
        },
    )
    ID = 0
    IMG_SRC = 1
    IMG_ALT = 2
    TITLE = 3
    MAIN_TEXT = 4
    return [
        QuestionSuggestion(
            id=r[ID],
            img_src=r[IMG_SRC],
            img_alt=r[IMG_ALT],
            title=r[TITLE],
            main_text=r[MAIN_TEXT],
        )
        for r in res
    ]


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


async def select_current_session_steps(session_id: str) -> int:
    res = await select_from(
        f"""
SELECT CONFIG_VALUE
FROM TB_SESSION_CONFIGURATION
WHERE SESSION_ID = %(session_id)s
	AND CONFIG_KEY = '{SESSION_STEPS_CONFIG_KEY}'
""",
        {"session_id": session_id},
    )
    if (
        len(res) == 0
        or len(res[0]) == 0
        or res[0][0] == None
        # or not isinstance(res[0][0], int)
    ):
        return DEFAULT_SESSION_STEPS
    try:
        return int(res[0][0])
    except:
        logger.exception("Cannot select current session steps")
        return DEFAULT_SESSION_STEPS


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


async def select_questionnaire_status_suggestions(
    questionnaire_status_id: id,
) -> List[QuestionSuggestion]:
    res = await select_from(
        f"""
SELECT ID, MAIN_TEXT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS
WHERE QUESTIONNAIRE_STATUS_ID = %(questionnaire_status_id)s
""",
        {"questionnaire_status_id": questionnaire_status_id},
    )
    ID = 0
    MAIN_TEXT = 1
    if res == None:
        return []
    return [
        QuestionSuggestion(
            id=r[ID],
            img_src="",
            img_alt="",
            title="",
            main_text=r[MAIN_TEXT],
        )
        for r in res
    ]


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.questionnaire_status_provider import (
        create_simple,
    )
    from data_questionnaire_agent.test.provider.session_configuration_provider import (
        create_session_configuration,
    )

    async def test_insert_questionnaire_status():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        check_qs = await select_questionnaire(new_qs.session_id)
        assert check_qs is not None
        assert len(check_qs) == 1
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_select_initial():
        question = await select_initial_question()
        assert question is not None
        print(question)

    async def test_select_initial():
        question = await select_initial_question()
        assert question is not None
        suggestions = await select_suggestions(question)
        assert len(suggestions) > 0
        for s in suggestions:
            print(s)

    async def test_insert_answer():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        session_id = qs.session_id
        test_answer = "Some answer whatsoever"
        id = await update_answer(session_id, test_answer)
        assert id is not None
        check_qs = await select_questionnaire(session_id)
        assert check_qs[0].answer == test_answer
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_select_answers():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        session_id = qs.session_id
        test_answer = "Some answer whatsoever"
        id = await update_answer(session_id, test_answer)
        assert id is not None
        check_answers = await select_questionnaire(session_id)
        assert len(check_answers.questions) > 0
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_session_configuration_save():
        session_configuration = create_session_configuration()
        saved = await save_session_configuration(session_configuration)
        assert isinstance(saved, SessionConfigurationEntry)
        assert saved.id is not None
        session_configuration = await select_session_configuration(saved.session_id)
        assert len(session_configuration.configuration_entries) > 0
        updated_id = await update_session_steps(saved.session_id, 10)
        assert updated_id == saved.id
        deleted = await delete_session_configuration(saved.id)
        assert deleted == 1

    async def test_select_current_session_steps():
        session_configuration = create_session_configuration()
        saved = await save_session_configuration(session_configuration)
        assert isinstance(saved, SessionConfigurationEntry)
        current_session_steps = await select_current_session_steps(saved.session_id)
        assert current_session_steps == DEFAULT_SESSION_STEPS
        deleted = await delete_session_configuration(saved.id)
        assert deleted == 1

    async def test_save_report():
        from data_questionnaire_agent.test.provider.advice_provider import (
            create_simple_advice,
        )

        advice = create_simple_advice()
        dummy_session = "12321231231231"
        id = await save_report(dummy_session, advice, 0)
        assert id is not None
        deleted = await delete_questionnaire_status(id)
        assert deleted == 1

    async def test_insert_questionnaire_status_suggestions():
        from data_questionnaire_agent.test.provider.question_answer_provider import (
            create_question_answer_with_possible_answers,
        )

        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        question_answer = create_question_answer_with_possible_answers()
        changed = await insert_questionnaire_status_suggestions(
            new_qs.id, question_answer
        )
        assert changed > 1
        possible_question_answers = await select_questionnaire_status_suggestions(
            new_qs.id
        )
        assert len(possible_question_answers) > 0
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    # asyncio.run(test_insert_questionnaire_status())
    # asyncio.run(test_select_initial())
    # asyncio.run(test_insert_answer())
    # asyncio.run(test_select_answers())
    asyncio.run(test_session_configuration_save())
    # asyncio.run(test_select_current_session_steps())
    # asyncio.run(test_save_report())
    # asyncio.run(test_insert_questionnaire_status_suggestions())
