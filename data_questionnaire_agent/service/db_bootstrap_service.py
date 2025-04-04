from pathlib import Path
from typing import Union

from psycopg import AsyncCursor

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.query_support import create_connection


async def execute_script(path: Path) -> Union[str, bool]:
    assert path.exists(), f"Path {path} does not exist."
    with open(path, "r") as file:
        sql_script = file.read()
    assert len(sql_script) > 0, "SQL script seems to be empty"

    conn = None
    try:
        conn = await create_connection()
        await conn.set_autocommit(True)
        async with conn.cursor() as cursor:
            exists = await table_exists("tb_session_configuration", cursor)
            if not exists or "create database" in sql_script.lower():
                # If there are no table or no questions the script is executed.
                cursor = await cursor.execute(sql_script)
            else:
                return False
        return True
    except Exception as e:
        logger.exception("Cannot execute script")
        return str(e)
    finally:
        if conn:
            await conn.close()


async def table_exists(table: str, cursor: AsyncCursor) -> bool:
    await cursor.execute(
        """
SELECT EXISTS (
   SELECT FROM information_schema.tables 
   WHERE  table_schema = 'public'
   AND    table_name   = %(table)s
   );
            """,
        {"table": table},
    )
    rows = await cursor.fetchone()
    return rows[0]
