import os
from enum import StrEnum
from pathlib import Path

import tenacity
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from tenacity import stop_after_attempt

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config_support import create_db_conn_str

load_dotenv()


class GraphRagMode(StrEnum):
    LOCAL = "local"
    GLOBAL = "global"
    ALL = "all"


def create_if_not_exists(folder):
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    assert folder.exists(), "Folder {folder} does not exist."


class Config:
    model = os.getenv("OPENAI_MODEL")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT"))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    streaming = os.getenv("CHATGPT_STREAMING") == "true"
    temperature = float(os.getenv("OPENAI_API_TEMPERATURE", 0.0))
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=streaming,
    )
    llm_stream = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=True,
    )
    logger.info(f"Using model {model}")

    image_llm_temperature = float(os.getenv("IMAGE_LLM_TEMPERATURE"))
    image_llm = OpenAI(temperature=image_llm_temperature)

    verbose_llm = os.getenv("VERBOSE_LLM") == "true"
    ui_timeout = int(os.getenv("UI_TIMEOUT"))
    project_root = Path(os.getenv("PROJECT_ROOT"))
    assert project_root.exists()
    question_cache_folder = os.getenv("QUESTION_CACHE_FOLDER")
    question_cache_folder_path = Path(question_cache_folder)

    create_if_not_exists(question_cache_folder_path)
    wkhtmltopdf_binary = Path(os.getenv("WKHTMLTOPDF_BINARY"))
    assert wkhtmltopdf_binary.exists(), f"Cannot find {wkhtmltopdf_binary}"
    template_location = Path(os.getenv("TEMPLATE_LOCATION"))
    assert template_location.exists()
    pdf_folder = Path(os.getenv("PDF_FOLDER"))
    create_if_not_exists(pdf_folder)
    jwt_gen_folder = Path(os.getenv("JWT_GEN_FOLDER"))
    create_if_not_exists(jwt_gen_folder)
    pdf_banner = Path(os.getenv("PDF_BANNER"))
    assert pdf_banner.exists(), f"Cannot find PDF banner: {pdf_banner}"

    # Embedding related
    raw_text_folder = Path(os.getenv("RAW_TEXT_FOLDER"))
    create_if_not_exists(raw_text_folder)
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

    product_title = "Hypergility Responsible AI Companion™"
    tracker_db_logs_password = os.getenv("TRACKER_DB_LOGS_PASSWORD")

    translation_path = os.getenv("TRANSLATION_PATH")
    assert Path(translation_path).exists()
    assert (
        translation_path is not None
    ), "Please specifiy the translation path TRANSLATION_PATH."

    aggregator_report_folder_str = os.getenv("AGGREGATOR_REPORT_FOLDER")
    assert (
        aggregator_report_folder_str is not None
    ), "The aggregator report is not None."
    aggregator_report_folder = Path(aggregator_report_folder_str)
    create_if_not_exists(aggregator_report_folder)

    use_graphrag = os.getenv("USE_GRAPHRAG") == "true"
    graphrag_base_url = os.getenv("GRAPHRAG_BASE_URL")
    if use_graphrag:
        assert (
            graphrag_base_url is not None
        ), "If you want to use Graphrag you should specify the base URL."
    graphrag_mode = os.getenv("GRAPHRAG_MODE")
    assert graphrag_mode in [
        GraphRagMode.LOCAL,
        GraphRagMode.GLOBAL,
        GraphRagMode.ALL,
    ], "GraphRAG mode not recognized"
    graphrag_context_size_str = os.getenv("GRAPHRAG_CONTEXT_SIZE", "10000")
    graphrag_context_size = int(graphrag_context_size_str)
    graphrag_jwt = os.getenv("GRAPHRAG_JWT")
    assert graphrag_jwt is not None, "JWT is needed to access GraphRAG server"
    graphrag_project = os.getenv("GRAPHRAG_PROJECT")
    assert graphrag_project is not None, "GraphRAG project is required."
    graphrag_read_timeout = float(os.getenv("GRAPHRAG_READ_TIMEOUT", "20"))


cfg = Config()


class MailConfig:
    mail_user = os.getenv("MAIL_USER")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")
    mail_server = os.getenv("MAIL_SERVER")
    mail_from_person = os.getenv("MAIL_FROM_PERSON")
    mail_to_name = os.getenv("MAIL_TO_NAME")
    mail_subject = os.getenv("MAIL_SUBJECT")
    feedback_email = os.getenv("FEEDBACK_EMAIL", "feedback@onepointltd.com")


mail_config = MailConfig()


class WebsocketConfig:
    websocket_server = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
    websocket_port = int(os.getenv("WEBSOCKET_PORT", 8080))
    websocket_cors_allowed_origins = os.getenv("WEBSOCKET_CORS_ALLOWED_ORIGINS", "*")


websocket_cfg = WebsocketConfig()


class WebServerConfig:
    ui_folder = Path(os.getenv("UI_FOLDER", "./web/ui"))
    if not ui_folder.exists():
        ui_folder.mkdir(parents=True, exist_ok=True)
    images_folder = Path(os.getenv("IMAGES_FOLDER", "./public/images"))
    assert images_folder.exists(), f"{images_folder} does not exist. Please create it."


web_server_cfg = WebServerConfig()


class DBConfig:
    db_create = os.getenv("DB_CREATE", "false") == "true"
    db_conn_str = create_db_conn_str()


db_cfg = DBConfig()


class JWTTokenConfig:
    secret = os.getenv("JWT_SECRET")
    assert secret is not None, "Cannot find JWT secret"
    algorithm = os.getenv("JWT_ALGORITHM")
    assert algorithm is not None, "Cannot find JWT algorithm"
    timedelta_minutes = os.getenv("JWT_TIME_DELTA_MINUTES")
    assert timedelta_minutes is not None, "No time delta in minutes available"
    timedelta_minutes = int(timedelta_minutes)
    dwell_url = os.getenv("DWELL_URL", "https://d-well.onepointltd.ai")
    dwise_url = os.getenv("DWISE_URL", "https://d-wise.onepointltd.ai")


jwt_token_cfg = JWTTokenConfig()


class ReportAggregationConfig:
    report_token_limit_str = os.getenv("REPORT_TOKEN_LIMIT", "30000")
    report_token_limit = int(report_token_limit_str)


report_agg_cfg = ReportAggregationConfig()


if __name__ == "__main__":
    logger.info("Model: %s", cfg.model)
    logger.info("Verbose: %s", cfg.verbose_llm)
    logger.info("mail_config user: %s", mail_config.mail_user)
    logger.info("wkhtmltopdf: %s", cfg.wkhtmltopdf_binary.as_posix())
    logger.info("template_location: %s", cfg.template_location.as_posix())

    logger.info("JWT_SECRET: %s", jwt_token_cfg.secret)
    logger.info("JWT_ALGORITHM: %s", jwt_token_cfg.algorithm)

    print(ReportAggregationConfig.report_token_limit)

    logger.info("GRAPHRAG_JWT: %s", cfg.graphrag_jwt)
