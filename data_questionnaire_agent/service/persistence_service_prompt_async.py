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
INSERT INTO TB_PROMPT_CATEGORY(NAME, PROMPT_CATEGORY_PARENT_ID, LANGUAGE_ID)
VALUES(%(name)s, %(prompt_category_parent_id)s, (SELECT ID FROM TB_LANGUAGE WHERE LANGUAGE_CODE = %(language_code)s))
ON CONFLICT (NAME, PROMPT_CATEGORY_PARENT_ID, LANGUAGE_ID) DO NOTHING
RETURNING ID, CREATED_AT
            """,
            {
                "name": prompt_category.name,
                "prompt_category_parent_id": prompt_category.prompt_category_parent_id,
                "language_code": prompt_category.language_code,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        created_at = created_row[1]
        return PromptCategory(
            id=created_id,
            name=prompt_category.name,
            language_code=prompt_category.language_code,
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
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, (SELECT LANGUAGE_CODE FROM TB_LANGUAGE WHERE ID = LANGUAGE_ID), CREATED_AT, UPDATED_AT
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
    LANGUAGE_CODE = 3
    CREATED_AT = 4
    UPDATED_AT = 5
    return PromptCategory(
        id=row[ID],
        name=row[NAME],
        prompt_category_parent_id=row[PROMPT_CATEGORY_PARENT_ID],
        language_code=row[LANGUAGE_CODE],
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
VALUES(%(prompt_category_id)s, %(prompt_key)s, %(prompt)s)
ON CONFLICT (PROMPT_CATEGORY_ID, PROMPT_KEY) DO NOTHING
RETURNING ID, CREATED_AT
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


prompts_cache = {}


async def clear_prompts_cache():
    prompts_cache.clear()


async def read_system_human_prompts(categories: list[str], language_code: str = "en") -> dict:
    if language_code in prompts_cache:
        cached = prompts_cache[language_code]
        current_path = cached.copy()
        for category in categories:
            if category not in current_path:
                return None
            current_path = current_path[category]
        return {
            "system_message": current_path["system_message"],
            "human_message": current_path["human_message"],
        }
    system_prompt = await read_prompt_by_prompt_key(categories, "system_message", language_code)
    human_prompt = await read_prompt_by_prompt_key(categories, "human_message", language_code)
    if system_prompt is None or human_prompt is None:
        raise ValueError("System or human prompt not found")
    return {
        "system_message": system_prompt.prompt,
        "human_message": human_prompt.prompt,
    }


async def get_prompts(language_code: str = "en") -> dict:
    if language_code in prompts_cache:
        return prompts_cache[language_code].copy()
    async def process_read(cur: AsyncCursor):
        sql = """
SELECT (WITH RECURSIVE CATS AS (
  SELECT PC.ID CAT_ID, PC.NAME AS CAT_NAME, prompt_category_parent_id, 1 AS LEVEL 
  	FROM TB_PROMPT_CATEGORY PC WHERE PC.ID = PC1.ID
  UNION ALL
  SELECT PC.ID CAT_ID, PC.NAME AS CAT_NAME, PC.prompt_category_parent_id, CATS.LEVEL + 1 AS LEVEL 
  	FROM CATS INNER JOIN TB_PROMPT_CATEGORY PC ON CATS.prompt_category_parent_id = PC.ID
)
SELECT PATH FROM (SELECT 1, STRING_AGG(CAT_NAME, '|' ORDER BY LEVEL DESC) AS PATH FROM CATS GROUP by 1)) AS PATH, 
PC1.ID category_id, PC1.NAME category_name, P.ID prompt_id, PROMPT_KEY, PROMPT, P.CREATED_AT, P.UPDATED_AT 
FROM TB_PROMPT P
INNER JOIN TB_PROMPT_CATEGORY PC1 ON P.PROMPT_CATEGORY_ID = PC1.ID
INNER JOIN TB_LANGUAGE L on L.ID = PC1.LANGUAGE_ID
WHERE L.LANGUAGE_CODE = %(language_code)s;
"""
        await cur.execute(sql, {"language_code": language_code})
        rows = await cur.fetchall()
        PATH = 0
        PROMPT_KEY = 4
        PROMPT = 5
        path_dict = {}
        for row in rows:
            current_path = path_dict
            paths = row[PATH].split("|")
            for path in paths:
                if path not in current_path:
                    current_path[path] = {}
                current_path = current_path[path]#
            current_path[row[PROMPT_KEY]] = row[PROMPT]
        prompts_cache[language_code] = path_dict
        return prompts_cache[language_code]

    return await create_cursor(process_read, True)


async def read_prompt_by_prompt_key(categories: list[str], prompt_key: str, language_code: str = "en") -> DBPrompt | None:
    if len(categories) == 0:
        return None
    async def process_read(cur: AsyncCursor):
        current_category: PromptCategory | None = None
        ID = 0
        NAME = 1
        PROMPT_CATEGORY_PARENT_ID = 2
        LANGUAGE_CODE = 3
        CREATED_AT = 4
        UPDATED_AT = 5
        for index, category in enumerate(categories):
            common_filters_sql = "NAME = %(category)s AND LANGUAGE_ID = (SELECT ID FROM TB_LANGUAGE WHERE LANGUAGE_CODE = %(language_code)s)"
            sql = """
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, (SELECT LANGUAGE_CODE FROM TB_LANGUAGE WHERE ID = LANGUAGE_ID), CREATED_AT, UPDATED_AT FROM TB_PROMPT_CATEGORY WHERE """ + common_filters_sql + """ AND PROMPT_CATEGORY_PARENT_ID = %(parent_id)s
"""
            params = {
                "category": category,
                "parent_id": current_category.id if current_category is not None else None,
                "language_code": language_code,
            }
            if index == 0:
                if "parent_id" in params:
                    del params["parent_id"]
                sql = """
SELECT ID, NAME, PROMPT_CATEGORY_PARENT_ID, (SELECT LANGUAGE_CODE FROM TB_LANGUAGE WHERE ID = LANGUAGE_ID), CREATED_AT, UPDATED_AT FROM TB_PROMPT_CATEGORY WHERE """ + common_filters_sql + """ AND PROMPT_CATEGORY_PARENT_ID is null
"""
            await cur.execute(sql, params)
            row = await cur.fetchone()
            if row is None:
                return None
            current_category = PromptCategory(id=row[ID], name=row[NAME], prompt_category_parent_id=row[PROMPT_CATEGORY_PARENT_ID], language_code=row[LANGUAGE_CODE], created_at=row[CREATED_AT], updated_at=row[UPDATED_AT])
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


if __name__ == "__main__":
    import asyncio
    import json
    res = asyncio.run(get_prompts("en"))
    json.dump(res, open("prompts.json", "w"), indent=4)