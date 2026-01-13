from pathlib import Path

import tomli

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d