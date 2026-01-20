from data_questionnaire_agent.service.context_service import extract_relevant_documents
from data_questionnaire_agent.test.provider.context_provider import (
    create_sample_context,
)


def test_extract_relevant_documents():
    context = create_sample_context()
    relevant_documents = extract_relevant_documents(context, most_common_count=10)
    assert len(relevant_documents.documents) == 10
    import json

    with open("data/relevant_documents.json", "w", encoding="utf-8") as f:
        json.dump(relevant_documents.model_dump(), f, indent=4)
