import os
from pathlib import Path

from dotenv import load_dotenv

from data_questionnaire_agent.config_support import create_db_conn_str

root_project = Path(__file__).resolve().parent.parent

load_dotenv((root_project / ".env").resolve().as_posix(), verbose=True)


class DBConfig:
    db_create = os.getenv("DB_CREATE", "false") == "true"
    db_conn_str = create_db_conn_str()


db_cfg = DBConfig()