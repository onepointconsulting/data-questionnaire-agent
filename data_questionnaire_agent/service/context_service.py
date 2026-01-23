from collections import Counter, defaultdict

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
    context: Context, most_common_count: int = 5
) -> ContextDocuments:
    document_extracts = defaultdict(list)
    relevant_documents = []
    relevant_documents_counter = Counter()
    count_documents(context.entities_context, relevant_documents_counter)
    count_documents(context.relations_context, relevant_documents_counter)
    count_documents(context.text_units_context, relevant_documents_counter)
    for entry in context.text_units_context:
        file_path = entry.file_path
        document_extracts[file_path].append(entry.content[:16384]) # 16384 is the max length of a document extract

    for file_path, extract_list in document_extracts.items():
        relevant_documents.append(
            ContextDocument(
                count=relevant_documents_counter.get(file_path, 1),
                document_path=file_path,
                document_name=file_path.split("/")[-1],
                document_extracts=extract_list,
            )
        )
    sorted_relevant_documents = sorted(relevant_documents, key=lambda x: x.count, reverse=True)
    return ContextDocuments(documents=sorted_relevant_documents[:most_common_count])
