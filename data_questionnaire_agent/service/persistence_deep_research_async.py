from psycopg import AsyncCursor

from data_questionnaire_agent.model.deep_research import (
    Citation,
    DeepResearchAdviceOutput,
    DeepResearchOutputs,
)
from data_questionnaire_agent.service.query_support import create_cursor, select_from


async def save_deep_research(
    session_id: str, advice: str, deep_research_output: DeepResearchAdviceOutput
) -> int | None:
    async def process(cur: AsyncCursor):
        sql = """
INSERT INTO TB_DEEP_RESEARCH_OUTPUT(SESSION_ID, ADVICE, OUTPUT) 
VALUES(%(session_id)s, %(advice)s, %(output)s) RETURNING ID;
"""
        await cur.execute(
            sql,
            {
                "session_id": session_id,
                "advice": advice,
                "output": deep_research_output.deep_research_output,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        for citation in deep_research_output.citations:
            sql = """
INSERT INTO TB_DEEP_RESEARCH_CITATION(DEEP_RESEARCH_OUTPUT_ID, TITLE, URL, START_INDEX, END_INDEX, TEXT)
VALUES(%(deep_research_output_id)s, %(title)s, %(url)s, %(start_index)s, %(end_index)s, %(text)s)
"""
            await cur.execute(
                sql,
                {
                    "deep_research_output_id": created_id,
                    "title": citation.title,
                    "url": citation.url,
                    "start_index": citation.start_index,
                    "end_index": citation.end_index,
                    "text": citation.text,
                },
            )
        return created_id

    return await create_cursor(process, True)


async def read_deep_research(
    session_id: str, advice: str | None = None
) -> DeepResearchOutputs:
    """
    Only the latest deep research output for the given advice will be returned.
    """
    sql = f"""
WITH INIT_QUERY AS
(SELECT ROW_NUMBER() OVER (PARTITION BY SESSION_ID, ADVICE ORDER BY CREATED_AT) deep_research_row_number, ID, ADVICE, OUTPUT FROM TB_DEEP_RESEARCH_OUTPUT WHERE SESSION_ID = %(session_id)s {"AND ADVICE = %(advice)s" if advice is not None else ""})
SELECT ID, ADVICE, OUTPUT FROM INIT_QUERY WHERE deep_research_row_number = 1
"""
    rows = await select_from(
        sql,
        (
            {"session_id": session_id}
            if advice is None
            else {"session_id": session_id, "advice": advice}
        ),
    )
    if rows is None:
        return []
    deep_research_outputs = []
    title_pos = 0
    url_pos = 1
    start_index_pos = 2
    end_index_pos = 3
    text_pos = 4
    for row in rows:
        deep_research_output_id = row[0]
        citations_sql = """
SELECT TITLE, URL, START_INDEX, END_INDEX, TEXT FROM TB_DEEP_RESEARCH_CITATION WHERE DEEP_RESEARCH_OUTPUT_ID = %(deep_research_output_id)s
"""
        citation_rows = rows = await select_from(
            citations_sql, {"deep_research_output_id": deep_research_output_id}
        )
        citations = [
            Citation(
                index=i,
                title=citation_row[title_pos],
                url=citation_row[url_pos],
                start_index=citation_row[start_index_pos],
                end_index=citation_row[end_index_pos],
                text=citation_row[text_pos],
            )
            for i, citation_row in enumerate(citation_rows)
        ]
        deep_research_outputs.append(
            DeepResearchAdviceOutput(
                advice=row[1], deep_research_output=row[2], citations=citations
            )
        )
    return DeepResearchOutputs(outputs=deep_research_outputs)


async def delete_deep_research(session_id: str) -> int:
    async def process(cur: AsyncCursor):
        sql = """
DELETE FROM TB_DEEP_RESEARCH_OUTPUT WHERE SESSION_ID = %(session_id)s
"""
        await cur.execute(sql, {"session_id": session_id})
        return cur.rowcount

    return await create_cursor(process, True)
