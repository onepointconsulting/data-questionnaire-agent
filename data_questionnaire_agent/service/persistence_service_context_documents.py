from collections import defaultdict
from psycopg import AsyncCursor

from data_questionnaire_agent.model.context_documents import (
    ContextDocument,
    ContextDocuments,
)
from data_questionnaire_agent.service.query_support import create_cursor


async def persist_context_documents(
    context_documents: ContextDocuments,
) -> ContextDocuments | None:
    async def process_save(cur: AsyncCursor):
        for context_document in context_documents.documents:
            await cur.execute(
                """
    INSERT INTO TB_CONTEXT_DOCUMENTS(DOCUMENT_PATH, DOCUMENT_NAME, COUNT, DOCUMENT_EXTRACT, QUESTIONNAIRE_STATUS_ID)
    VALUES(%(document_path)s, %(document_name)s, %(count)s, %(document_extract)s, %(questionnaire_status_id)s)
    ON CONFLICT (DOCUMENT_PATH, QUESTIONNAIRE_STATUS_ID) DO NOTHING
    RETURNING ID, CREATED_AT
                """,
                {
                    "document_path": context_document.document_path,
                    "document_name": context_document.document_name,
                    "count": context_document.count,
                    "document_extract": context_document.document_extract,
                    "questionnaire_status_id": context_documents.questionnaire_status_id,
                },
            )
            created_row = await cur.fetchone()
            if created_row is None or len(created_row) == 0:
                return None
            context_document.id = created_row[0]
        return context_documents

    return await create_cursor(process_save, True)


async def delete_context_documents(questionnaire_status_id: int) -> int:
    async def process_delete(cur: AsyncCursor):
        await cur.execute(
            """
DELETE FROM TB_CONTEXT_DOCUMENTS WHERE QUESTIONNAIRE_STATUS_ID = %(questionnaire_status_id)s
            """,
            {"questionnaire_status_id": questionnaire_status_id},
        )
        return cur.rowcount

    return await create_cursor(process_delete, True)


async def read_context_documents(
    questionnaire_status_ids: list[int],
) -> list[ContextDocuments] | None:
    async def process_read(cur: AsyncCursor):
        await cur.execute(
            """
SELECT ID, DOCUMENT_PATH, DOCUMENT_NAME, COUNT, DOCUMENT_EXTRACT, QUESTIONNAIRE_STATUS_ID, CREATED_AT, UPDATED_AT
FROM TB_CONTEXT_DOCUMENTS WHERE QUESTIONNAIRE_STATUS_ID = ANY(%(questionnaire_status_ids)s)
            """,
            {"questionnaire_status_ids": questionnaire_status_ids},
        )
        rows = await cur.fetchall()
        if len(rows) == 0:
            return None
        ID = 0
        DOCUMENT_PATH = 1
        DOCUMENT_NAME = 2
        COUNT = 3
        DOCUMENT_EXTRACT = 4
        QUESTIONNAIRE_STATUS_ID = 5
        context_documents_dict = defaultdict(list)
        for row in rows:
            context_document = ContextDocument(
                id=row[ID],
                document_path=row[DOCUMENT_PATH],
                document_name=row[DOCUMENT_NAME],
                count=row[COUNT],
                document_extract=row[DOCUMENT_EXTRACT],
            )
            context_documents_dict[row[QUESTIONNAIRE_STATUS_ID]].append(context_document)
        context_documents_list = []
        for questionnaire_status_id, context_documents in context_documents_dict.items():
            context_documents_list.append(ContextDocuments(
                questionnaire_status_id=questionnaire_status_id,
                documents=context_documents,
            ))
        return context_documents_list

    return await create_cursor(process_read, True)
