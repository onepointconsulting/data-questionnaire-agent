from psycopg import AsyncCursor

from data_questionnaire_agent.model.application_schema import QuestionAnswer
from data_questionnaire_agent.model.question_suggestion import (
    QuestionAndSuggestions,
    QuestionInfo,
    QuestionSuggestion,
)
from data_questionnaire_agent.service.query_support import create_cursor, select_from
from data_questionnaire_agent.toml_support import get_prompts


async def select_initial_question(language: str) -> tuple[int, str]:
    first_question = (await select_questions(language))[0]
    return (first_question[0], first_question[1])


async def select_questions(language: str) -> list[tuple[int, str]]:
    res = await select_from(
        """
SELECT Q.id, Q.question FROM TB_QUESTION Q INNER JOIN public.tb_language L on Q.language_id = L.id
WHERE LANGUAGE_CODE = %(language)s
ORDER BY PREFERRED_QUESTION_ORDER
""",
        {"language": language},
    )
    if res is None or len(res) == 0:
        return [(0, get_prompts(language)["questionnaire"]["initial"]["question"])]
    return [(row[0], row[1]) for row in res]


async def select_outstanding_questions(
    language: str, session_id: str
) -> list[QuestionAnswer]:
    sql = """
        SELECT Q.ID, TRIM(Q.QUESTION)
        FROM PUBLIC.TB_QUESTION Q
        WHERE Q.LANGUAGE_ID =
        (SELECT ID
        FROM PUBLIC.TB_LANGUAGE LANGUAGE_CODE
        WHERE LANGUAGE_CODE = %(language)s)
        AND NOT EXISTS
        (SELECT S.QUESTION_ID
        FROM TB_QUESTIONNAIRE_STATUS S
        WHERE S.SESSION_ID = %(session_id)s
            AND Q.ID = S.QUESTION_ID)
        ORDER BY Q.PREFERRED_QUESTION_ORDER;
    """

    res = await select_from(sql, {"language": language, "session_id": session_id})
    if res is None:
        return []
    question_answers = []
    for r in res:
        id = r[0]
        question = r[1]
        possible_answers = await select_suggestions_string(id)
        questionanswer = QuestionAnswer(
            id=id,
            question=question,
            answer="",
            possible_answers=[],
            clarification=[],
        )
        questionanswer.possible_answers.extend(possible_answers)
        question_answers.append(questionanswer)
    return question_answers


async def select_question_and_suggestions(
    language: str,
) -> list[QuestionAndSuggestions]:
    questions = await select_questions(language)
    question_and_suggestions = []
    for question in questions:
        suggestions = await select_suggestions(question[1])
        question_and_suggestions.append(
            QuestionAndSuggestions(
                id=question[0], question=question[1], suggestions=suggestions
            )
        )
    return QuestionInfo(question_and_suggestions=question_and_suggestions)


async def update_question(id: int, question: str, suggestions: list[dict]) -> int:
    async def delete_suggestions_process(cur: AsyncCursor, id: int):
        # First get all the question suggestion IDs.
        get_existing_suggestion_ids_sql = """
        SELECT S.id FROM public.tb_question_suggestions S
        INNER JOIN public.tb_question Q ON Q.id = S.question_id
        WHERE Q.id = %(id)s;
        """

        await cur.execute(get_existing_suggestion_ids_sql, {"id": id})
        rows = await cur.fetchall()

        # And then we need to loop through the suggestions and extract the IDs
        existing_suggestion_ids = {row[0] for row in rows}

        incoming_suggestion_ids = {suggestion["id"] for suggestion in suggestions}

        ids_to_delete = existing_suggestion_ids - incoming_suggestion_ids

        if ids_to_delete:
            await cur.execute(
                "DELETE FROM public.tb_question_suggestions WHERE id = ANY(%(ids)s)",
                {"ids": list(ids_to_delete)},
            )

    async def insert_and_update_suggestions_process(
        cur: AsyncCursor, suggestions: list[dict], id: int
    ):
        insert_suggestion_sql = """
        INSERT INTO PUBLIC.TB_QUESTION_SUGGESTIONS (ID, IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID, SVG_IMAGE)
        SELECT (SELECT NEXTVAL('public.tb_question_suggestions_id_seq')), 
        %(img_src)s, %(img_alt)s, %(title)s, %(main_text)s, %(question_id)s, %(svg_image)s
        WHERE NOT EXISTS (SELECT ID FROM TB_QUESTION_SUGGESTIONS WHERE ID = %(id)s);
        """

        update_suggestion_sql = """
        UPDATE PUBLIC.TB_QUESTION_SUGGESTIONS
        SET 
        IMG_SRC = %(img_src)s,
        IMG_ALT = %(img_alt)s,
        TITLE = %(title)s,
        MAIN_TEXT = %(main_text)s,
        QUESTION_ID = %(question_id)s,
        SVG_IMAGE = %(svg_image)s
        WHERE ID = %(id)s;
        """

        if len(suggestions) > 0:
            for suggestion in suggestions:
                question_suggestion = QuestionSuggestion(**suggestion)
                await cur.execute(
                    insert_suggestion_sql,
                    {
                        "img_src": "",
                        "img_alt": "",
                        "title": question_suggestion.title,
                        "main_text": question_suggestion.main_text,
                        "question_id": id,
                        "svg_image": question_suggestion.svg_image,
                        "id": question_suggestion.id,
                    },
                )
                if cur.rowcount == 0:
                    await cur.execute(
                        update_suggestion_sql,
                        {
                            "img_src": "",
                            "img_alt": "",
                            "title": question_suggestion.title,
                            "main_text": question_suggestion.main_text,
                            "question_id": id,
                            "svg_image": question_suggestion.svg_image,
                            "id": question_suggestion.id,
                        },
                    )

    async def process_update(cur: AsyncCursor):
        updated_question_count = 0
        await cur.execute(
            """
            UPDATE TB_QUESTION
            SET QUESTION = %(question)s
            WHERE ID = %(id)s
            """,
            {"id": id, "question": question},
        )

        updated_question_count = cur.rowcount

        await delete_suggestions_process(cur, id)
        await insert_and_update_suggestions_process(cur, suggestions, id)
        return updated_question_count

    return await create_cursor(process_update, True)


async def insert_question(
    question: str, language_code: str, suggestions: list[dict]
) -> int | None:
    async def process_create(cur: AsyncCursor):
        await cur.execute(
            """
            INSERT INTO TB_QUESTION(QUESTION, LANGUAGE_ID)
            VALUES(%(question)s, (SELECT ID FROM TB_LANGUAGE WHERE LANGUAGE_CODE = %(language_code)s))
            RETURNING ID
            """,
            {"question": question, "language_code": language_code},
        )
        rows = await cur.fetchone()
        if len(rows) == 0:
            return None
        new_id = rows[0]
        for suggestion in suggestions:
            await cur.execute(
                """
                INSERT INTO TB_QUESTION_SUGGESTIONS(img_src, img_alt, title, main_text, question_id, svg_image)
                VALUES(%(img_src)s, %(img_alt)s, %(title)s, %(main_text)s, %(question_id)s, %(svg_image)s)
                RETURNING ID
                """,
                {
                    "img_src": suggestion["img_src"],
                    "img_alt": suggestion["img_alt"],
                    "title": suggestion["title"],
                    "main_text": suggestion["main_text"],
                    "question_id": new_id,
                    "svg_image": suggestion["svg_image"],
                },
            )
            assert cur.rowcount > 0, "Failed to insert suggestion"
        return new_id

    return await create_cursor(process_create, True)


async def delete_question(id: int) -> int:
    async def process_delete(cur: AsyncCursor):
        await cur.execute(
            """
            DELETE FROM TB_QUESTION_SUGGESTIONS
            WHERE QUESTION_ID = (%(id)s)
            """,
            {"id": id},
        )
        await cur.execute(
            """
            DELETE FROM TB_QUESTION
            WHERE ID = (%(id)s)
            """,
            {"id": id},
        )
        return cur.rowcount

    return await create_cursor(process_delete, True)


async def select_suggestions(question: str) -> list[QuestionSuggestion]:
    res = await select_from(
        """SELECT S.id, img_src, img_alt, title, main_text, svg_image FROM TB_QUESTION_SUGGESTIONS S 
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
wHERE Q.question = %(question)s
ORDER BY S.ID""",
        {
            "question": question,
        },
    )
    ID = 0
    IMG_SRC = 1
    IMG_ALT = 2
    TITLE = 3
    MAIN_TEXT = 4
    SVG_IMAGE = 5
    return [
        QuestionSuggestion(
            id=r[ID],
            img_src=r[IMG_SRC],
            img_alt=r[IMG_ALT],
            title=r[TITLE],
            main_text=r[MAIN_TEXT],
            svg_image=r[SVG_IMAGE] or "",
        )
        for r in res
    ]


async def select_suggestions_string(id: int) -> list[QuestionSuggestion]:
    res = await select_from(
        """SELECT main_text FROM TB_QUESTION_SUGGESTIONS S 
wHERE S.question_id = %(id)s
ORDER BY S.ID""",
        {
            "id": id,
        },
    )
    return [r[0] for r in res]
