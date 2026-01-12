from data_questionnaire_agent.model.prompt import PromptCategory
from data_questionnaire_agent.model.prompt import DBPrompt
from data_questionnaire_agent.service.query_support import create_cursor

from psycopg import AsyncCursor


async def persist_prompt_category(
    prompt_category: PromptCategory,
) -> PromptCategory | None:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_PROMPT_CATEGORY(NAME, PROMPT_CATEGORY_PARENT_ID)
VALUES(%(name)s, %(prompt_category_parent_id)s) RETURNING ID, CREATED_AT
            """,
            {
                "name": prompt_category.name,
                "prompt_category_parent_id": prompt_category.prompt_category_parent_id,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        created_at = created_row[1]
        return PromptCategory(
            id=created_id,
            name=prompt_category.name,
            prompt_category_parent_id=prompt_category.prompt_category_parent_id,
            created_at=created_at,
            updated_at=prompt_category.updated_at,
        )

    return await create_cursor(process_save, True)


async def _read_prompt_category(
    cur: AsyncCursor, prompt_category_id: int
) -> PromptCategory | None:
    await cur.execute(
        """
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, CREATED_AT, UPDATED_AT
FROM TB_PROMPT_CATEGORY WHERE ID = %(prompt_category_id)s
        """,
        {"prompt_category_id": prompt_category_id},
    )

    row = await cur.fetchone()
    if row is None:
        return None
    ID = 0
    NAME = 1
    PROMPT_CATEGORY_PARENT_ID = 2
    CREATED_AT = 3
    UPDATED_AT = 4
    return PromptCategory(
        id=row[ID],
        name=row[NAME],
        prompt_category_parent_id=row[PROMPT_CATEGORY_PARENT_ID],
        created_at=row[CREATED_AT],
        updated_at=row[UPDATED_AT],
    )


async def read_prompt_category(prompt_category_id: int) -> PromptCategory | None:
    async def process_read(cur: AsyncCursor):
        return await _read_prompt_category(cur, prompt_category_id)

    return await create_cursor(process_read, True)  #


async def delete_prompt_category(prompt_category_id: int) -> None:
    async def process_delete(cur: AsyncCursor):
        result = await cur.execute(
            """
DELETE FROM TB_PROMPT_CATEGORY WHERE ID = %(prompt_category_id)s
            """,
            {"prompt_category_id": prompt_category_id},
        )
        return result.rowcount

    return await create_cursor(process_delete, True)


async def persist_prompt(prompt: DBPrompt) -> DBPrompt | None:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_PROMPT(PROMPT_CATEGORY_ID, PROMPT_KEY, PROMPT)
VALUES(%(prompt_category_id)s, %(prompt_key)s, %(prompt)s) RETURNING ID, CREATED_AT
            """,
            {
                "prompt_category_id": prompt.prompt_category.id,
                "prompt_key": prompt.prompt_key,
                "prompt": prompt.prompt,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        created_at = created_row[1]
        return DBPrompt(
            id=created_id,
            prompt_category=prompt.prompt_category,
            prompt_key=prompt.prompt_key,
            prompt=prompt.prompt,
            created_at=created_at,
            updated_at=prompt.updated_at,
        )

    return await create_cursor(process_save, True)


async def read_prompt_by_prompt_key(categories: list[str], prompt_key: str) -> DBPrompt | None:
    if len(categories) == 0:
        return None
    async def process_read(cur: AsyncCursor):
        current_category: PromptCategory | None = None
        ID = 0
        NAME = 1
        PROMPT_CATEGORY_PARENT_ID = 2
        CREATED_AT = 3
        UPDATED_AT = 4
        for index, category in enumerate(categories):
            sql = """
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, CREATED_AT, UPDATED_AT FROM TB_PROMPT_CATEGORY WHERE NAME = %(category)s AND PROMPT_CATEGORY_PARENT_ID = %(parent_id)s
"""
            params = {
                "category": category,
                "parent_id": current_category.id if current_category is not None else None
            }
            if index == 0:
                if "parent_id" in params:
                    del params["parent_id"]
                sql = """
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, CREATED_AT, UPDATED_AT FROM TB_PROMPT_CATEGORY WHERE NAME = %(category)s AND PROMPT_CATEGORY_PARENT_ID is null
"""
            await cur.execute(sql, params)
            row = await cur.fetchone()
            if row is None:
                return None
            current_category = PromptCategory(id=row[ID], name=row[NAME], prompt_category_parent_id=row[PROMPT_CATEGORY_PARENT_ID], created_at=row[CREATED_AT], updated_at=row[UPDATED_AT])
        await cur.execute(
            """
SELECT ID, PROMPT_CATEGORY_ID, PROMPT_KEY, PROMPT, CREATED_AT, UPDATED_AT
FROM TB_PROMPT WHERE PROMPT_CATEGORY_ID = %(prompt_category_id)s AND PROMPT_KEY = %(prompt_key)s
""", {
"prompt_category_id": current_category.id,
"prompt_key": prompt_key
})
        row = await cur.fetchone()
        if row is None:
            return None
        ID = 0
        
        PROMPT_KEY = 2
        PROMPT = 3
        CREATED_AT = 4
        UPDATED_AT = 5
        return DBPrompt(id=row[ID], prompt_category=current_category, prompt_key=row[PROMPT_KEY], prompt=row[PROMPT], created_at=row[CREATED_AT], updated_at=row[UPDATED_AT])
    return await create_cursor(process_read, True)


async def read_prompt(prompt_id: int) -> DBPrompt | None:
    async def process_read(cur: AsyncCursor):
        await cur.execute(
            """
SELECT ID, PROMPT_CATEGORY_ID, PROMPT_KEY, PROMPT, CREATED_AT, UPDATED_AT
FROM TB_PROMPT WHERE ID = %(prompt_id)s
            """,
            {"prompt_id": prompt_id},
        )
        row = await cur.fetchone()
        if row is None:
            return None
        ID = 0
        PROMPT_CATEGORY_ID = 1
        PROMPT_KEY = 2
        PROMPT = 3
        CREATED_AT = 4
        UPDATED_AT = 5
        prompt_category = await _read_prompt_category(cur, row[PROMPT_CATEGORY_ID])
        return DBPrompt(
            id=row[ID],
            prompt_category=prompt_category,
            prompt_key=row[PROMPT_KEY],
            prompt=row[PROMPT],
            created_at=row[CREATED_AT],
            updated_at=row[UPDATED_AT],
        )

    return await create_cursor(process_read, True)


async def delete_prompt(prompt_id: int) -> None:
    async def process_delete(cur: AsyncCursor):
        result = await cur.execute(
            """
DELETE FROM TB_PROMPT WHERE ID = %(prompt_id)s
            """,
            {"prompt_id": prompt_id},
        )
        return result.rowcount

    return await create_cursor(process_delete, True)
