from pathlib import Path

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.embedding_service import (
    generate_embeddings,
    load_text,
)

from langchain.vectorstores import FAISS


def init_vector_search() -> FAISS:
    embedding_dir = cfg.embeddings_persistence_dir.as_posix()
    embedding_dir_path = Path(embedding_dir)
    # Check if directory exists and has something inside
    if embedding_dir_path.exists() and len(list(embedding_dir_path.glob("*"))) > 0:
        logger.info(f"reading from existing directory")
        docsearch = FAISS.load_local(embedding_dir, cfg.embeddings)
        return docsearch
    else:
        logger.warning(f"Cannot find path {embedding_dir} or path is empty.")
        doc_location = cfg.raw_text_folder
        logger.info(f"Using doc location {doc_location}.")
        logger.info("Generating vectors")
        documents = load_text(path=doc_location)
        docsearch = generate_embeddings(
            documents=documents, persist_directory=embedding_dir
        )
        return docsearch
    

def similarity_search(docsearch: FAISS, input: str, how_many=cfg.search_results_how_many) -> str:
    doc_list = docsearch.similarity_search(input, k=how_many)
    logger.info("Similarity search results: %s", len(doc_list))
    return "\n\n".join([p.page_content for p in doc_list])
    

if __name__ == "__main__":
    docsearch = init_vector_search()
    search_res = similarity_search(docsearch, "Data Quality")
    print(search_res)

