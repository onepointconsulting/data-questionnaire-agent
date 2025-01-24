from psycopg import AsyncCursor

from data_questionnaire_agent.model.question_suggestion import (
    QuestionAndSuggestions,
    QuestionInfo,
    QuestionSuggestion,
)
from data_questionnaire_agent.service.query_support import create_cursor, select_from
from data_questionnaire_agent.toml_support import get_prompts


async def select_initial_question(language: str) -> str:
    return (await select_questions(language))[0][1]


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
        update_suggestion_sql = """
UPDATE PUBLIC.TB_QUESTION_SUGGESTIONS
SET IMG_SRC = %(img_src)s,
	IMG_ALT = %(img_alt)s,
	TITLE = %(title)s,
	MAIN_TEXT = %(main_text)s,
	QUESTION_ID = %(question_id)s,
	SVG_IMAGE = %(svg_image)s
WHERE ID = %(id)s
"""
        if len(suggestions) > 0:
            for suggestion in suggestions:
                question_suggestion = QuestionSuggestion(**suggestion)
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
        return updated_question_count

    return await create_cursor(process_update, True)


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
