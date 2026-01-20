from collections import Counter

from data_questionnaire_agent.model.context import (
    Context,
    EntityContextEntry,
    RelationsContextEntry,
    TextUnitContextEntry,
)
from data_questionnaire_agent.model.context_documents import (
    ContextDocument,
    ContextDocuments,
)


def find_document_extract(document_path: str, context: Context) -> str:
    for entity in context.text_units_context:
        if entity.file_path == document_path:
            return entity.content
    return ""


def split_file_path(file_path: str) -> list[str]:
    return file_path.split("<SEP>")


def count_documents(
    entities: list[EntityContextEntry]
    | list[RelationsContextEntry]
    | list[TextUnitContextEntry],
    relevant_documents_counter: Counter,
):
    for entity in entities:
        for single_path in split_file_path(entity.file_path):
            relevant_documents_counter[single_path] += 1


def extract_relevant_documents(
    context: Context, most_common_count: int = 10
) -> ContextDocuments:
    relevant_documents = []
    relevant_documents_counter = Counter()
    count_documents(context.entities_context, relevant_documents_counter)
    count_documents(context.relations_context, relevant_documents_counter)
    count_documents(context.text_units_context, relevant_documents_counter)
    for document_path, count in relevant_documents_counter.most_common(
        most_common_count
    ):
        relevant_documents.append(
            ContextDocument(
                count=count,
                document_path=document_path,
                document_name=document_path.split("/")[-1],
                document_extract=find_document_extract(document_path, context),
            )
        )
    return ContextDocuments(documents=relevant_documents)
