# import debugpy

# debugpy.listen(5678)


from pathlib import Path
import os

from dotenv import load_dotenv
from tenacity import stop_after_attempt
import tenacity

from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


from langchain_community.vectorstores import FAISS

# from langchain.llms import OpenAI
from langchain_openai import OpenAI

load_dotenv()

from data_questionnaire_agent.log_init import logger


def create_if_not_exists(folder):
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    assert folder.exists(), "Folder {folder} does not exist."


class Config:
    model = os.getenv("OPENAI_MODEL")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT"))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    streaming = os.getenv("CHATGPT_STREAMING") == "true"
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=0,
        request_timeout=request_timeout,
        cache=False,
        streaming=streaming,
    )

    image_llm_temperature = float(os.getenv("IMAGE_LLM_TEMPERATURE"))
    image_llm = OpenAI(temperature=image_llm_temperature)

    verbose_llm = os.getenv("VERBOSE_LLM") == "true"
    ui_timeout = int(os.getenv("UI_TIMEOUT"))
    project_root = Path(os.getenv("PROJECT_ROOT"))
    print("\n✴️  project_root", project_root)
    assert project_root.exists()
    question_cache_folder = os.getenv("QUESTION_CACHE_FOLDER")
    question_cache_folder_path = Path(question_cache_folder)

    create_if_not_exists(question_cache_folder_path)
    wkhtmltopdf_binary = Path(os.getenv("WKHTMLTOPDF_BINARY"))
    
    assert wkhtmltopdf_binary.exists()
    template_location = Path(os.getenv("TEMPLATE_LOCATION"))
    print(f"\n✴️ template_location", template_location)

    assert template_location.exists() #template_location.is_dir()
    pdf_folder = Path(os.getenv("PDF_FOLDER"))
    create_if_not_exists(pdf_folder)
    use_tasklist = os.getenv("TASKLIST") == "true"
    show_chain_of_thought = os.getenv("SHOW_CHAIN_OF_THOUGHT") == "true"

    # Embedding related
    raw_text_folder = Path(os.getenv("RAW_TEXT_FOLDER"))
    embeddings_persistence_dir = Path(os.getenv("EMBEDDINGS_PERSISTENCE_DIR"))
    chunk_size = int(os.getenv("EMBEDDINGS_CHUNK_SIZE"))
    embeddings = OpenAIEmbeddings(chunk_size=chunk_size)
    
    
    search_results_how_many = int(os.getenv("SEARCH_RESULTS_HOW_MANY"))
    token_limit = int(os.getenv("TOKEN_LIMIT"))

    # Questions
    questions_per_batch = int(os.getenv("QUESTIONS_PER_BATCH"))
    minimum_questionnaire_size = int(os.getenv("MINIMUM_QUESTIONNAIRE_SIZE"))

    # Session cost
    show_session_cost = os.getenv("SHOW_SESSION_COST") == "true"
    openai_retry_attempts = int(os.getenv("OPENAI_RETRY_ATTEMPTS"))
    wait_fixed = int(os.getenv("OPENAI_WAIT_FIXED"))

    retry_args = {
        "stop": stop_after_attempt(openai_retry_attempts),
        "wait": tenacity.wait_fixed(wait_fixed),
    }

    product_title = "Onepoint Data Wellness Companion™"
    tracker_db_logs_password = os.getenv("TRACKER_DB_LOGS_PASSWORD")


cfg = Config()


class MailConfig:
    mail_user = os.getenv("MAIL_USER")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")
    mail_server = os.getenv("MAIL_SERVER")
    mail_from_person = os.getenv("MAIL_FROM_PERSON")
    mail_to_name = os.getenv("MAIL_TO_NAME")
    mail_subject = os.getenv("MAIL_SUBJECT")


mail_config = MailConfig()

if __name__ == "__main__":
    logger.info("Model: %s", cfg.model)
    logger.info("Verbose: %s", cfg.verbose_llm)
    logger.info("mail_config user: %s", mail_config.mail_user)
    logger.info("wkhtmltopdf: %s", cfg.wkhtmltopdf_binary.as_posix())
    logger.info("template_location: %s", cfg.template_location.as_posix())
    logger.info("use_tasklist: %s", cfg.use_tasklist)
