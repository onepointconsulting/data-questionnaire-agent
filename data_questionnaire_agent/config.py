import asyncio
from enum import StrEnum
from pathlib import Path

import tenacity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from tenacity import stop_after_attempt

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.global_configuration import GlobalConfiguration


class GraphRagMode(StrEnum):
    LOCAL = "local"
    GLOBAL = "global"
    ALL = "all"


def create_if_not_exists(folder):
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    assert folder.exists(), "Folder {folder} does not exist."



def convert_global_configuration_cfg_to_dict() -> dict:
    from data_questionnaire_agent.service.persistence_service_async import select_global_configuration
    global_configuration_cfg: GlobalConfiguration = asyncio.run(select_global_configuration())
    return {prop.config_key: prop.config_value for prop in global_configuration_cfg.properties}


global_configuration_dict = convert_global_configuration_cfg_to_dict()


class Config:
    model = global_configuration_dict.get("OPENAI_MODEL")
    deep_research_model = global_configuration_dict.get("DEEP_RESEARCH_MODEL")
    request_timeout = int(global_configuration_dict.get("REQUEST_TIMEOUT"))
    has_langchain_cache = global_configuration_dict.get("LANGCHAIN_CACHE") == "true"
    streaming = global_configuration_dict.get("CHATGPT_STREAMING") == "true"
    temperature = float(global_configuration_dict.get("OPENAI_API_TEMPERATURE", 0.0))
    llm = ChatOpenAI(
        openai_api_key=global_configuration_dict.get("OPENAI_API_KEY"),
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=streaming,
    )
    llm_stream = ChatOpenAI(
        openai_api_key=global_configuration_dict.get("OPENAI_API_KEY"),
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=True,
    )
    logger.info(f"Using AI model {model}")

    verbose_llm = global_configuration_dict.get("VERBOSE_LLM") == "true"
    ui_timeout = int(global_configuration_dict.get("UI_TIMEOUT", "60"))
    project_root = Path(
        global_configuration_dict.get("PROJECT_ROOT", Path(__file__).resolve().parent.parent)
    )
    assert project_root.exists()
    question_cache_folder = global_configuration_dict.get(
        "QUESTION_CACHE_FOLDER", Path(__file__).resolve().parent.parent
    )
    question_cache_folder_path = Path(question_cache_folder)

    create_if_not_exists(question_cache_folder_path)
    wkhtmltopdf_binary = Path(global_configuration_dict.get("WKHTMLTOPDF_BINARY"))
    assert wkhtmltopdf_binary.exists(), f"Cannot find {wkhtmltopdf_binary}"
    template_location = Path(__file__).resolve().parent.parent / "templates"
    assert template_location.exists(), f"Cannot find {template_location}"
    pdf_folder = Path(global_configuration_dict.get("PDF_FOLDER"))
    create_if_not_exists(pdf_folder)
    jwt_gen_folder = Path(global_configuration_dict.get("JWT_GEN_FOLDER"))
    create_if_not_exists(jwt_gen_folder)

    # Embedding related
    raw_text_folder = Path(global_configuration_dict.get("RAW_TEXT_FOLDER"))
    create_if_not_exists(raw_text_folder)
    embeddings_persistence_dir = Path(global_configuration_dict.get("EMBEDDINGS_PERSISTENCE_DIR"))
    chunk_size = int(global_configuration_dict.get("EMBEDDINGS_CHUNK_SIZE"))
    embeddings = OpenAIEmbeddings(
        chunk_size=chunk_size, openai_api_key=global_configuration_dict.get("OPENAI_API_KEY")
    )
    search_results_how_many = int(global_configuration_dict.get("SEARCH_RESULTS_HOW_MANY"))
    token_limit = int(global_configuration_dict.get("TOKEN_LIMIT"))

    # Questions
    questions_per_batch = int(global_configuration_dict.get("QUESTIONS_PER_BATCH"))
    minimum_questionnaire_size = int(global_configuration_dict.get("MINIMUM_QUESTIONNAIRE_SIZE"))

    # Session cost
    show_session_cost = global_configuration_dict.get("SHOW_SESSION_COST") == "true"
    openai_retry_attempts = int(global_configuration_dict.get("OPENAI_RETRY_ATTEMPTS"))
    wait_fixed = int(global_configuration_dict.get("OPENAI_WAIT_FIXED"))

    retry_args = {
        "stop": stop_after_attempt(openai_retry_attempts),
        "wait": tenacity.wait_fixed(wait_fixed),
    }

    product_title = global_configuration_dict.get("PRODUCT_TITLE", "Onepoint Data Wellness Companion™")

    translation_path = Path(__file__).resolve().parent.parent / "i18n"
    assert Path(translation_path).exists()
    assert (
        translation_path is not None
    ), "Please specifiy the translation path TRANSLATION_PATH."

    aggregator_report_folder_str = global_configuration_dict.get("AGGREGATOR_REPORT_FOLDER")
    assert (
        aggregator_report_folder_str is not None
    ), "The aggregator report is not None."
    aggregator_report_folder = Path(aggregator_report_folder_str)
    create_if_not_exists(aggregator_report_folder)

    use_graphrag = global_configuration_dict.get("USE_GRAPHRAG") == "true"
    graphrag_base_url = global_configuration_dict.get("GRAPHRAG_BASE_URL")
    if use_graphrag:
        assert (
            graphrag_base_url is not None
        ), "If you want to use Graphrag you should specify the base URL."
    graphrag_mode = global_configuration_dict.get("GRAPHRAG_MODE")
    assert graphrag_mode in [
        GraphRagMode.LOCAL,
        GraphRagMode.GLOBAL,
        GraphRagMode.ALL,
    ], "GraphRAG mode not recognized"
    graphrag_context_size_str = global_configuration_dict.get("GRAPHRAG_CONTEXT_SIZE", "10000")
    graphrag_context_size = int(graphrag_context_size_str)
    graphrag_jwt = global_configuration_dict.get("GRAPHRAG_JWT")
    assert graphrag_jwt is not None, "JWT is needed to access GraphRAG server"
    graphrag_project = global_configuration_dict.get("GRAPHRAG_PROJECT")
    assert graphrag_project is not None, "GraphRAG project is required."
    graphrag_read_timeout = float(global_configuration_dict.get("GRAPHRAG_READ_TIMEOUT", "20"))
    graphrag_engine = global_configuration_dict.get("GRAPHRAG_ENGINE", "lightrag")


cfg = Config()


class MailConfig:
    mail_user = global_configuration_dict.get("MAIL_USER")
    mail_password = global_configuration_dict.get("MAIL_PASSWORD")
    mail_from = global_configuration_dict.get("MAIL_FROM")
    mail_server = global_configuration_dict.get("MAIL_SERVER")
    mail_from_person = global_configuration_dict.get("MAIL_FROM_PERSON")
    mail_to_name = global_configuration_dict.get("MAIL_TO_NAME")
    mail_subject = global_configuration_dict.get("MAIL_SUBJECT")
    feedback_email = global_configuration_dict.get("FEEDBACK_EMAIL", "feedback@onepointltd.com")


mail_config = MailConfig()


class WebsocketConfig:
    websocket_server = global_configuration_dict.get("WEBSOCKET_SERVER", "0.0.0.0")
    websocket_port = int(global_configuration_dict.get("WEBSOCKET_PORT", 8080))
    logger.info(f"Websocket server: {websocket_server}")
    logger.info(f"Websocket port: {websocket_port}")
    websocket_cors_allowed_origins = global_configuration_dict.get("WEBSOCKET_CORS_ALLOWED_ORIGINS", "*")


websocket_cfg = WebsocketConfig()


class WebServerConfig:
    ui_folder = Path(__file__).resolve().parent.parent / "ui"
    if not ui_folder.exists():
        ui_folder.mkdir(parents=True, exist_ok=True)
    images_folder = Path(__file__).resolve().parent.parent / "public" / "images"
    assert images_folder.exists(), f"{images_folder} does not exist. Please create it."


web_server_cfg = WebServerConfig()


class JWTTokenConfig:
    secret = global_configuration_dict.get("JWT_SECRET")
    assert secret is not None, "Cannot find JWT secret"
    algorithm = global_configuration_dict.get("JWT_ALGORITHM")
    assert algorithm is not None, "Cannot find JWT algorithm"
    timedelta_minutes = global_configuration_dict.get("JWT_TIME_DELTA_MINUTES")
    assert timedelta_minutes is not None, "No time delta in minutes available"
    timedelta_minutes = int(timedelta_minutes)
    dwell_url = global_configuration_dict.get("DWELL_URL", "https://d-well.onepointltd.ai")
    dwise_url = global_configuration_dict.get("DWISE_URL", "https://d-wise.onepointltd.ai")


jwt_token_cfg = JWTTokenConfig()


class ReportAggregationConfig:
    report_token_limit_str = global_configuration_dict.get("REPORT_TOKEN_LIMIT", "30000")
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
