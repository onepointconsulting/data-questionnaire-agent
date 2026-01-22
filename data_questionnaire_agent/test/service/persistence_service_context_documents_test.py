import pytest

from data_questionnaire_agent.model.context_documents import (
    ContextDocument,
    ContextDocuments,
)
from data_questionnaire_agent.service.persistence_service_async import (
    delete_questionnaire_status,
    insert_questionnaire_status,
)
from data_questionnaire_agent.service.persistence_service_context_documents import (
    persist_context_documents,
    read_context_documents,
)
from data_questionnaire_agent.test.provider.questionnaire_status_provider import (
    create_simple,
)


@pytest.mark.asyncio
async def test_persist_and_read_context_documents():
    questionnaire_status = None
    try:
        questionnaire_status = create_simple()
        new_questionnaire_status = await insert_questionnaire_status(
            questionnaire_status
        )
        context_documents = ContextDocuments(
            questionnaire_status_id=new_questionnaire_status.id,
            documents=[
                ContextDocument(
                    id=None,
                    document_path="test_document_path",
                    document_name="test_document_name",
                    count=1,
                    document_extract="test_document_extract",
                )
            ],
        )
        new_context_documents = await persist_context_documents(context_documents)
        assert new_context_documents is not None
        assert len(new_context_documents.documents) == 1
        new_context_documents_from_db = await read_context_documents(
            [new_questionnaire_status.id]
        )
        assert new_context_documents_from_db is not None
        assert len(new_context_documents_from_db[0].documents) == 1
        assert new_context_documents_from_db[0].documents[0].id is not None
        assert (
            new_context_documents_from_db[0].documents[0].document_path
            == "test_document_path"
        )
        assert (
            new_context_documents_from_db[0].documents[0].document_name
            == "test_document_name"
        )
        assert new_context_documents_from_db[0].documents[0].count == 1
        assert (
            new_context_documents_from_db[0].documents[0].document_extract
            == "test_document_extract"
        )
    finally:
        deleted = await delete_questionnaire_status(new_questionnaire_status.id)
        assert deleted == 1
