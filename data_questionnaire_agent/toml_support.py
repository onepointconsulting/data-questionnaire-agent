from pathlib import Path

import tomli

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger


def read_toml(file: Path) -> dict:
    with open(file, "rb") as f:
        return tomli.load(f)


# Need to add a language parameter.
# Pick the right file based on the language parameter.
# Default to English if the language is not supported.

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "de"]


def read_prompts_toml(language: str = DEFAULT_LANGUAGE) -> dict:
    if language not in SUPPORTED_LANGUAGES:
        logger.warn(
            f"Warning: language {language} not supported. Using default language."
        )
        language = DEFAULT_LANGUAGE

    logger.warn(f"Reading prompts from prompts_{language}.toml")
    return read_toml(cfg.project_root / f"{cfg.prompts_prefix}_{language}.toml")


prompts_language = {}
for lang in SUPPORTED_LANGUAGES:
    prompts_language[lang] = read_prompts_toml(lang)


def get_prompts(language: str = DEFAULT_LANGUAGE) -> dict:
    if language in prompts_language:
        return prompts_language[language]
    return prompts_language[DEFAULT_LANGUAGE]


def get_prompts_object(language: str = DEFAULT_LANGUAGE) -> object:
    prompts = get_prompts(language)
    return objectview(prompts)


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d