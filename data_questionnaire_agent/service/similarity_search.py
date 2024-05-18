from pathlib import Path
from typing import List

import tiktoken
# from langchain.vectorstores import FAISS
# from langchain_community.vectorstores import FAISS
# from langchain_community.vectorstores.faiss import FAISS
# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS

# from langchain_community.vectorstores import FAISS

from langchain.schema import Document

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.embedding_service import (
    generate_embeddings,
    load_text,
)


def init_vector_search() -> FAISS:
    embedding_dir = cfg.embeddings_persistence_dir.as_posix()
    embedding_dir_path = Path(embedding_dir)
    # Check if directory exists and has something inside
    if embedding_dir_path.exists() and len(list(embedding_dir_path.glob("*"))) > 0:
        logger.info(f"reading from existing directory")
        docsearch = FAISS.load_local(
            embedding_dir, cfg.embeddings, allow_dangerous_deserialization=True
        )
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


def join_pages(doc_list: List[Document]) -> str:
    return "\n\n".join([p.page_content for p in doc_list])


def similarity_search(
    docsearch: FAISS, input: str, how_many=cfg.search_results_how_many
) -> str:
    """
    Performs multiple searches until it reaches the maximum amount of tokens below a specified threshold.
    When the threshold of tokens is reached it stops and returns the search results.

    Parameters:
    docsearch FAISS: The object used to access the vector database.
    input str: The input of the search.
    how_many int: The initial number of results to be retrieved.

    Returns:
    str: The maximum amount of text with the number of tokens below the threshold specified in the configuration.
    """
    token_count = 0
    previous_res = ""
    attempts = 0
    max_attempts = 4
    while attempts < max_attempts:
        doc_list = docsearch.similarity_search(input, k=how_many + attempts)        
        logger.info("Similarity search results: %s", len(doc_list))
        joined = join_pages(doc_list)
        token_count = num_tokens_from_string(joined)
        logger.info("Token count: %d", token_count)
        attempts += 1
        if token_count > cfg.token_limit:
            return previous_res
        previous_res = joined
    return previous_res


def num_tokens_from_string(string: str) -> int:
    """
    Returns the number of tokens in a text string.

    Parameters:
    string (str): The string for which the tiktokens are to be counted.

    Returns:
    int: Recturs the number of tokens generated using tiktoken.
    """
    encoding = tiktoken.encoding_for_model(cfg.model)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    docsearch = init_vector_search()
    search_res = similarity_search(docsearch, "Data Quality")
    print(search_res)
    print(num_tokens_from_string(search_res))
